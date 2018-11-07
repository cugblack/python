#!/usr/binn/env python
# -*- coding: utf-8 -*-
import thread

from time import sleep, ctime
def loop1():
    print "loop 1 start sleep at : ", ctime()
    sleep(4)
    print "loop 1 done at : ", ctime()

def loop2():
    print "loop 2 start at : ", ctime()
    sleep(2)
    print "loop 2 done at : ", ctime()

def main():
    print "all start at : ", ctime()
    #并发执行两个程序
    thread.start_new_thread(loop1, ())
    thread.start_new_thread(loop2, ())
    # 因为主线程不停止的话，会接着继续执行打印，此时线程loop1还为运行完，主线程退出会关闭在运行的程序
    sleep(6)
    print "all done at : ", ctime()

if __name__ == "__main__":
    main()

'''
#执行结果
all start at :  Wed Nov 07 17:22:58 2018
loop 1 start sleep at :  Wed Nov 07 17:22:58 2018
loop 2 start at :  Wed Nov 07 17:22:58 2018
loop 2 done at :  Wed Nov 07 17:23:00 2018
loop 1 done at :  Wed Nov 07 17:23:02 2018
all done at :  Wed Nov 07 17:23:04 2018
'''