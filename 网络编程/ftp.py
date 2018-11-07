#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  ftplib, os, socket

HOST = "ftp.mozilla.org"
DIRN = "pub/webtools"
FILE = "bugzilla-4.4.13.tar.gz"

def main():
    try:
        f = ftplib.FTP(HOST)
    except (socket.error, socket.gaierror),e:
        print "cannot reach %s" % HOST
        return
    print "connected to host: %s" %HOST
    #登录
    try:
        f.login()
    except ftplib.error_perm:
        print "login failed!"
        f.quit()
        return
    #切换路径
    try:
        f.cwd(DIRN)
    except ftplib.error_perm:
        print "cannot cd to dir :%s" % DIRN
        f.quit()
        return
    #下载文件
    try:
        f.retrbinary("Retry %s" % FILE, open(FILE, "wb").write)
    except ftplib.error_perm:
        print "ERROR: cannot read file %s" % FILE
        os.unlink(FILE)
    else:
        print "Download %s to CWD" % FILE
    f.quit()
    return
if __name__ == "__main__":
    main()

