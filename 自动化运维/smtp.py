#!/usr/bin/env python

import smtplib, string

HOST = "smtp.gmail.com"
SUBJECT = "test"
TO = "to_who@qq.com"
FROM = "cugblack@gmail.com"
text = "python test"
BODY = string.join(( 
         "From: %s" % FROM,
         "To  : %s" % TO,
         "Subject: %s" % SUBJECT,
         "",
         text
         ),"\r\n")
server = smtplib.SMTP()
server.connect(HOST,"25")
server.starttls()
server.login("yourmail@gmail.com","yourpassword")
server.sendmail(FROM, [TO], BODY)
server.quit()

