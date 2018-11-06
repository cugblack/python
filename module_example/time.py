#!/usr/binn/env python
# -*- coding: utf-8 -*-
#时间格式转换
import time
#时间戳转换为%Y-%m-%d %H:%M:%S格式的时间
timestamp = 1381419600
timeArray = time.localtime(timestamp)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print  otherStyleTime
#%Y-%m-%d %H:%M:%S格式的时间转换为时间戳
a = "2013-10-10 18:40:00"
#必须先将时间格式化  strptim():根据fmt的格式把一个时间字符串解析为时间元组。
otherTime = time.strptime(a, "%Y-%m-%d %H:%M:%S")
STAMP_TIME = int(time.mktime(otherTime))
print STAMP_TIME