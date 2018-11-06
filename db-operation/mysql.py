#!/usr/binn/env python
# -*- coding: utf-8 -*-
import pymysql, time, config
from pymysql import err
from exceptions import Exception
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SQL = "SELECT t.* FROM cloud.app t LIMIT 5"
FILE = "E:\\desktop\\sum.csv"

def db_conn(SQL):
    try:
        conn = pymysql.connect(config.MYSQL_HOST, config.MYSQL_USER, config.MYSQL_PASSWD, config.MYSQL_DB)
        cursor = conn.cursor()
    except err.MySQLError:
        print err.MySQLError
    try:
        cursor.execute(SQL)
        # RESULT = cursor.fetchone() #取结果集中的一个值
        RESULTS = cursor.fetchall()   #取结果集的所有值
        return RESULTS
    except err.OperationalError:
        print "exec sql err", err.OperationalError
    conn.close()

def time_transfer(TIME_STAMP):
    #将时间戳转换为 2018-09-12 10：11：04格式的时间
    TIME_ARRAY = time.localtime(TIME_STAMP)
    OTHER_STYLE_TIME = time.strftime("%Y-%m-%d %H:%M:%S", TIME_ARRAY)
    return  OTHER_STYLE_TIME

def file_out(SQL, FILE):
#写入结果到csv文件中
    RESULTS = db_conn(SQL)
    try:
        fo = open(FILE,"w")
        fo.write("ID,TIME,PROJECT_ID")
        for res in RESULTS:
            ID = res[0]
            START_TIME = time_transfer(res[8])  # 时间为时间戳，先转换格式
            PROJECT_ID = res[4]
            fo.write("{},{},{}\n".format(ID, START_TIME, PROJECT_ID))
    except Exception:
        print "写入文件失败", Exception
    fo.close()


def retry():
    import os
    # os.remove("E:\\desktop\\sum.csv")
    file_out(SQL, FILE)

def main():
    file_out(SQL, FILE)

if __name__ == "__main__":
    main()