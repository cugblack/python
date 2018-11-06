#_*_ coding=utf-8
import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def mail():
    from datetime import date
    msg = MIMEMultipart()
    msg["from"] = config.SENDER_MAIL
    msg["to"] = config.TO
    msg["subject"] = u"测试邮件"
    txt = MIMEText(u"这是一封带附件的测试邮件。", "plain", "utf-8")
    msg.attach(txt)
    TIME = date.today()
    PATH = "E:\\"
    # 构造附件
    att = MIMEText(open(PATH + u"2018-06-29-temp.zip", "rb").read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = "attachment; filename= '2018-06-29-temp.zip' "
    msg.attach(att)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(config.HOST, "25")
        state = smtpObj.login(config.SENDER_MAIL, config.MAIL_AUTH)
        if state[0] == 235:
            smtpObj.sendmail(msg["from"], msg["to"], msg.as_string())
            print "邮件于 %s 发送给 %s 成功" % (TIME, config.TO)
            smtpObj.quit()
    except smtplib.SMTPException as e:
        print e

if __name__ == "__main__":
    mail()
