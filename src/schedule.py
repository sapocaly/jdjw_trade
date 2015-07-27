#! /usr/bin/env python
# coding=utf-8
import time
import os
import sched
import datetime

schedule = sched.scheduler(time.time, time.sleep)


def perform_command():
    ##do something
    os.system("python fetch_data.py &")
    now =  datetime.datetime.now()
    delta = (1000000 - now.microsecond) / 1000000.0
    schedule.enter(delta, 0, perform_command, ())




schedule.enter(1, 0, perform_command, ())
schedule.run()