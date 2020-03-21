#!/usr/bin/env bash
# -*- coding: UTF-8 -*-
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import os.path
import subprocess
import time
import socket
from multiprocessing import Pool
from kafka import KafkaConsumer
from kafka import TopicPartition

import paramiko
from enginedao.host import HostDao
from enginedao.workerprofile import WorkerProfileDao
from enginedao import host

from cloudriver import instance
from cloudriver import vpc

import config
import logger_util
import notify

logger = logger_util.get_logger(name='chworker.py')

KAFKA_HOST = config.KAFKA_HOST
KAFKA_TOPIC = config.KAFKA_TOPIC

try:
    KAFKA_PORT = int(config.KAFKA_PORT)
except Exception as e:
    logger.error(e)
    KAFKA_PORT = None

INSTANCE_NOT_RESOURCE = 'not_resource'


k_consumer = KafkaConsumer(KAFKA_TOPIC, group_id='g_scaling', bootstrap_servers='%s:%d' % (KAFKA_HOST, KAFKA_PORT),
                           value_deserializer=lambda v: json.loads(v.decode('utf-8')), enable_auto_commit=False)

try:
    PROCESS_NUM = len(k_consumer.partitions_for_topic(KAFKA_TOPIC))  # topic's partitions.
except Exception as e:
    logger.warning(e)
    PROCESS_NUM = 2


def __is_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return 'OK'
    except:
        return 'ERROR'

logger.info('Checking connection to Kafka, INFO:')
logger.info('Host: %s' % KAFKA_HOST)
logger.info('Port: %s' % KAFKA_PORT)
logger.info('Topic: %s' % KAFKA_TOPIC)
logger.info('Status: %s' % __is_open(KAFKA_HOST, KAFKA_PORT))


def multi_consumer():
    """
    Multi process consumer. rely on topic partitions.
    :return:
    """
    p = Pool(PROCESS_NUM)
    for i in range(PROCESS_NUM):
        p.apply_async(consumer)
    p.close()
    p.join()


def consumer():
    """
    Consumer kafka message.
    :return:
    """
    try:
        for msg in k_consumer:
            topic_partition = TopicPartition(KAFKA_TOPIC, msg.partition)
            k_consumer.seek(topic_partition, msg.offset + 1)
            k_consumer.commit()
            task_id = msg.key
            if 'add_' in task_id:  # Add instance
                msg_value = msg.value
                host_class = msg_value.get('host_class', None)
                is_spot = msg_value.get('is_spot', None)
                host_id = msg_value.get('host_id', None)
                host_name = msg_value.get('host_name', None)
                add(host_class=host_class, is_spot=is_spot, host_id=host_id, host_name=host_name)
            elif 'stop_' in task_id:  # Stop instance
                msg_value = msg.value
                host_id = msg_value.get('host_id', None)
                instance_id = msg_value.get('instance_id', None)
                stop(host_id=host_id, instance_id=instance_id)
    except KeyboardInterrupt as e:
        logger.error('Catch keyboard interrupt, stop consumer process!!!')


def add(host_class=None, is_spot=None, host_id=None, host_name=None):
    """
    Add instance.
    :param host_class:
    :param is_spot:
    :param host_id:
    :param host_name:
    :return:
    """

    logger.debug('**** Start update host status.')
    try:
        host_dao = HostDao()
        host_bean = host_dao.load(host_id)
        if host_bean:
            host_dao.update_status(host_id, host.HOST_STATUS_REQUESTING)  # Update host status to 'requesting'
        else:
            logger.error('Load host (%s) error, please check the host info in database.' % host_id)
            return
    except Exception as ex:
        logger.error(ex)
        __update_host_failed(host_bean, host_dao, ex)
        return
    logger.debug('**** End update host status.')

    try:
        worker_profile_dao = WorkerProfileDao()
        worker_profile = worker_profile_dao.load(host_class)
    except Exception as ae:
        logger.error(ae)
        __update_host_failed(host_bean, host_dao, ae)
        return

    if not worker_profile:
        workerp_msg = 'Load workerprofile from database error, host_class is %s' % host_class
        logger.error(workerp_msg)
        __update_host_failed(host_bean, host_dao, workerp_msg)
        return

    logger.info('host_id=%s, host_name=%s, host_class=%s, is_spot=%s' % (host_id, host_name, host_class, is_spot))

    image_id = worker_profile.image_id
    instance_type = worker_profile.instance_type
    password = config.CLOUD_PASSWORD
    region_id = worker_profile.region_id
    vpc_id = worker_profile.vpc_id
    zone_id = worker_profile.zone_id
    system_disk_category = config.CLOUD_SYSTEM_DISK_CATEGORY
    system_disk_size = config.CLOUD_SYSTEM_DISK_SIZE

    security_group_id = worker_profile_dao.SEPARATOR.join(worker_profile.security_group_ids)
    user_data = None
    if worker_profile.user_data:
        user_data = worker_profile.user_data.encode('base64')

    if is_spot:  # Spot instance, TODO next
        pass
    else:  # Demand instance
        vs_default_id = __get_vswitch_by_zone_id(vpc_id=vpc_id, zone_id=zone_id, region_id=region_id)  # Default VSwitch
        if vs_default_id:  # Default VSwitch
            instance_id = __create_demand_instance(image_id=image_id, instance_type=instance_type,
                                                   instance_name=host_name, password=password,
                                                   security_group_id=security_group_id, region_id=region_id,
                                                   vswitch_id=vs_default_id, user_data=user_data,
                                                   host_name=host_name, system_disk_category=system_disk_category,
                                                   system_disk_size=system_disk_size)

            if instance_id == INSTANCE_NOT_RESOURCE:  # Resource limit, retry other VSwitch
                logger.info('Default VSwitch (%s) has not resource types (%s), change other VSwitch.'
                            % (zone_id, instance_type))
                instance_id = __create_other_vswitch_instance(image_id=image_id, instance_type=instance_type,
                                                              instance_name=host_name, password=password,
                                                              security_group_id=security_group_id,
                                                              region_id=region_id, vpc_id=vpc_id,
                                                              default_zone_id=zone_id, user_data=user_data,
                                                              host_name=host_name, system_disk_size=system_disk_size,
                                                              system_disk_category=system_disk_category)
        else:  # Other VSwitch
            logger.info('Default VSwitch (%s) is None, change other VSwitch.' % zone_id)
            instance_id = __create_other_vswitch_instance(image_id=image_id, instance_type=instance_type,
                                                          instance_name=host_name, password=password,
                                                          security_group_id=security_group_id,
                                                          region_id=region_id, vpc_id=vpc_id,
                                                          default_zone_id=zone_id, user_data=user_data,
                                                          host_name=host_name, system_disk_size=system_disk_size,
                                                          system_disk_category=system_disk_category)

    if instance_id and instance_id != INSTANCE_NOT_RESOURCE:
        logger.debug('Create instance success, instance_id=%s' % instance_id)
        try:
            host_bean.instance_id = instance_id
            host_bean.status = host.HOST_STATUS_BOOTING
            host_bean.region_id = region_id
            host_dao.save(host_bean)  # Save host to database

            running_flag = instance.check_host_status_to_running(region_id=region_id, instance_id=instance_id)

            if running_flag:  # Create instance success.
                host_bean.status = host.HOST_STATUS_SETTING_UP
                host_dao.save(host_bean)  # Save host to database
                if not user_data:
                    __init_instance(region_id=region_id, instance_id=instance_id)  # Init instance
            else:
                __update_host_failed(host_bean, host_dao, None)

        except Exception as ex:
            logger.error(ex)
            __force_delete_instance(instance_id, region_id)
            __update_host_failed(host_bean, host_dao, ex)
    else:
        __update_host_failed(host_bean, host_dao, None)
        err_msg = 'All zones has not instance type (%s), vpc=%s, please change other instance type.' \
                  % (instance_type, vpc_id)
        notify.notify_admin(err_msg)


def stop(host_id=None, instance_id=None):
    """
    Stop instance.
    :param host_id:
    :param instance_id:
    :return:
    """
    logger.info('MQ stop instance, host_id=%s, instance_id=%s' % (host_id, instance_id))
    try:
        host_dao = HostDao()
        host_bean = host_dao.load(host_id)
        if host_bean:
            region_id = host_bean.region_id
            host_bean.status = host.HOST_STATUS_TERMINATING
            host_bean.is_deleted = True
            host_bean.touch()
        else:
            logger.error('Load host (%s) error, please check the host info in database.')
            return
    except Exception as ex:
        logger.error(ex)
        return

    if instance_id:
        __force_delete_instance(instance_id, region_id)  # Delete instance

    time.sleep(5)  # Sleep 5 second, wait the instance

    host_dao.save(host_bean)  # Save host to database


def __create_other_vswitch_instance(image_id, instance_type, instance_name, password,
                                    security_group_id, region_id, vpc_id, default_zone_id, user_data,
                                    host_name, system_disk_category, system_disk_size):
    """
    Create other VSwitch instance.
    :param image_id:
    :param instance_type:
    :param instance_name:
    :param password:
    :param security_group_id:
    :param region_id:
    :param vpc_id:
    :param default_zone_id:
    :param user_data:
    :param host_name:
    :param system_disk_category:
    :param system_disk_size:
    :return:
    """

    vswitchs = __describe_vswitches(vpc_id=vpc_id, region_id=region_id, default_zone_id=default_zone_id)
    instance_id = None
    if not vswitchs:
        return instance_id
    for vss in vswitchs:
        vss_zone_id = vss.get('zone_id')
        vss_vswitch_id = vss.get('vswitch_id')

        logger.info('Change other VSwitch, zone_id=%s, vswitch_id=%s' % (vss_zone_id, vss_vswitch_id))

        instance_id = __create_demand_instance(image_id=image_id, instance_type=instance_type,
                                               instance_name=instance_name, password=password,
                                               security_group_id=security_group_id, region_id=region_id,
                                               vswitch_id=vss_vswitch_id, user_data=user_data, host_name=host_name,
                                               system_disk_category=system_disk_category,
                                               system_disk_size=system_disk_size)
        if instance_id and instance_id != INSTANCE_NOT_RESOURCE:  # Create instance success.
            break

    return instance_id


def __create_demand_instance(image_id=None, instance_type=None, instance_name=None, password=None,
                             security_group_id=None, region_id=None, vswitch_id=None, user_data=None,
                             host_name=None, system_disk_category=None, system_disk_size=None):
    """
    Create demand instance which status is stopped.
    :param image_id:
    :param instance_type:
    :param instance_name:
    :param password:
    :param security_group_id:
    :param region_id:
    :param vswitch_id:
    :param user_data:
    :param host_name:
    :param system_disk_category:
    :param system_disk_size:
    :return: when success, return instance_id, when fail, return None or error message.
    """
    try:
        instance_id = instance.create_instance(image_id=image_id, instance_type=instance_type,
                                               instance_name=instance_name, password=password,
                                               security_group_id=security_group_id, region_id=region_id,
                                               vswitch_id=vswitch_id, user_data=user_data,
                                               host_name=host_name, system_disk_category=system_disk_category,
                                               system_disk_size=system_disk_size, io_optimized='optimized')

    except Exception as create_instance_e:
        err_msg = 'image_id=%s, instance_type=%s, instance_name=%s, region_id=%s, vswitch_id=%s, ' \
                  'host_name=%s \n\nException: \n %s' % (image_id, instance_type, instance_name, region_id,
                                                         vswitch_id, host_name, create_instance_e)
        logger.error(err_msg)
        notify.notify_admin(err_msg)
        instance_id = __retry_create_instance(create_instance_e.message)
    return instance_id


def __describe_vswitches(vpc_id=None, default_zone_id=None, region_id=None):
    """
    Describe VSwitches and filter default zone id
    :param vpc_id:
    :param default_zone_id:
    :param region_id:
    :return: [{'zone_id':'cn-shenzhen','vswitch_id':'vsw_sfedxeu321d'}]
    """
    result = None
    try:
        result = vpc.describe_vswitches(vpc_id=vpc_id, default_zone_id=default_zone_id, region_id=region_id)
    except Exception as dve:
        logger.error(dve)
    return result


def __get_vswitch_by_zone_id(vpc_id=None, zone_id=None, region_id=None):
    """
    Get vswitch by vpc_id and zone_id
    :param vpc_id:
    :param zone_id:
    :param region_id:
    :return: String (VSwitchId) or None
    """
    result = None
    logger.info('Get VSwitch info, vpc_id=%s, zone_id=%s, region_id=%s' % (vpc_id, zone_id, region_id))
    try:
        result = vpc.get_vswitch_by_zone_id(vpc_id=vpc_id, zone_id=zone_id, region_id=region_id)
    except Exception as dve:
        logger.error(dve)
    return result


def __force_delete_instance(instance_id=None, region_id=None):
    """
    Force delete instance
    :param instance_id:
    :return:
    """
    flag = True
    count = 0
    response = None
    while flag and count < 5:
        try:
            response = instance.delete_instance(instance_id=instance_id, force=True, region_id=region_id)
            flag = False
        except Exception as del_e:
            err_msg = 'instance_id=%s, region_id=%s. \n\n Exception: \n %s' % (instance_id, region_id, del_e)
            logger.error(err_msg)
            notify.notify_admin(err_msg)
        count += 1
        time.sleep(5)

    logger.info('Send message to delete instance (%s) success, request_id = %s' % (instance_id, response))


def __retry_create_instance(msg):
    """
    Error messages, some error messages can retry.
    :param msg:
    :return:
    """
    if 'This resource type is not supported' in msg:
        return INSTANCE_NOT_RESOURCE
    elif 'The requested resource is sold out in the specified zone' in msg:
        return INSTANCE_NOT_RESOURCE
    else:
        return None


def __update_host_failed(host_bean, host_dao, msg=None):
    """
    Update host status to request_failed and is_delete to true
    :param host_bean:
    :param host_dao:
    :return:
    """
    if msg:
        notify.notify_admin(msg)

    host_bean.status = host.HOST_STATUS_REQUEST_FAILED
    host_bean.is_deleted = True
    host_bean.touch()
    host_dao.save(host_bean)  # Save host to database


def __init_instance(region_id, instance_id):
    """
    Init instance, scp file to instance and run it.
    :param region_id:
    :param instance_id:
    :return:
    """

    logger.info('Start init instance...')
    vpc_id = instance.get_vpc_ip_by_id(region_id=region_id, instance_id=instance_id)
    user = config.CLOUD_USER
    password = config.CLOUD_PASSWORD
    worker_profile = config.CLOUD_WORKER_PROFILE_PATH
    if not worker_profile:
        msg = 'Load workerprofile (%s) is error, please check the config file.' % worker_profile
        notify.notify_admin(msg)
        logger.error(msg)
        __force_delete_instance(instance_id, region_id)
        return
    file_name = os.path.basename(worker_profile)

    tmp_instance_path = '/tmp/%s_sge_woker_init.conf' % instance_id

    instance_info = {'instance_id': instance_id}
    with open(tmp_instance_path, 'w') as f:
        f.write(json.dumps(instance_info))

    instance_cmd = ['sshpass', '-p', password, 'scp', '-o UserKnownHostsFile=/dev/null',
                    '-o StrictHostKeyChecking=no', tmp_instance_path,
                    '%s@%s:/root/sge_woker_init.conf' % (user, vpc_id)]

    __scp_file(instance_cmd)

    del_tmp_instance_path = ['rm', '-f', tmp_instance_path]

    try:
        subprocess.Popen(del_tmp_instance_path)  # Delete template file
    except Exception as del_e:
        logger.error(del_e)

    scp_cmd = ['sshpass', '-p', password, 'scp', '-o UserKnownHostsFile=/dev/null',
               '-o StrictHostKeyChecking=no', worker_profile, '%s@%s:/tmp/%s' % (user, vpc_id, file_name)]

    return_code = __scp_file(scp_cmd)

    if 0 == return_code:
        logger.info('Scp %s to host success.' % worker_profile)
        exe_cmd = 'sh /tmp/%s' % file_name
        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(vpc_id, 22, user, password)
            stdin, stdout, stderr = ssh.exec_command(exe_cmd)
            channel = stdout.channel
            status = channel.recv_exit_status()
            if stdout:
                for out_line in stdout.readlines():
                    logger.info(out_line.strip('\n'))
            if stderr:
                for err_line in stderr.readlines():
                    logger.error(err_line.strip('\n'))
            if 0 == status:
                logger.info('Init workerprofile success...')
            else:
                logger.error('Init wokerprofile error, please check the workerprofile.sh script.')
                __force_delete_instance(instance_id, region_id)
        except Exception as exec_e:
            logger.error(exec_e)
            __force_delete_instance(instance_id, region_id)
            raise Exception(exec_e)
        finally:
            ssh.close()
    else:
        raise Exception('Scp to worker error, cmd=%s' % scp_cmd)


def __scp_file(scp_cmd):
    """
    Copy file via command.
    :param scp_cmd:
    :return:
    """
    return_code = 1
    retry_num = 0

    while retry_num < 5 and return_code != 0:  # Retry 5 times
        try:
            return_code = subprocess.call(scp_cmd)
            logger.debug('scp file: %s, return_code: %s' % (scp_cmd, return_code))
        except subprocess.CalledProcessError as scp_e:
            notify.notify_admin(scp_e)
            logger.error(scp_e)
        retry_num += 1
        time.sleep(5)

    return return_code

if __name__ == '__main__':
    multi_consumer()
