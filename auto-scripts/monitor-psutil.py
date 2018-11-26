#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil
CPU_COUNT = psutil.cpu_count()
#CPU使用状况
CUP_USE = psutil.cpu_times()
#所有进程
PID_COUNT = psutil.pids()
#流入流出流量
TOTAL_OUTPUT_TRAFIC = psutil.net_io_counters()[0]
TOTAL_INPUT_TRAFIC = psutil.net_io_counters()[1]

print(CPU_COUNT, "\n", CUP_USE,"\n", PID_COUNT, "\n" ,TOTAL_INPUT_TRAFIC, TOTAL_OUTPUT_TRAFIC)
