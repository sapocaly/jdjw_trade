#! /usr/bin/env python
# coding=utf-8
import time
import os
import sched
import datetime

import logging
import logging.config

schedule = sched.scheduler(time.time, time.sleep)

logging.config.fileConfig("../conf/jdjw_trade_logger.cfg")
logger = logging.getLogger("jdjw_trade_fetch_digest")

def perform_command():
    ##do something
    logger.info('starting python')
    os.system("python fetch_data.py &")
    now =  datetime.datetime.now()
    delta = (1100000 - now.microsecond) / 1000000.0
    schedule.enter(delta, 0, perform_command, ())




schedule.enter(1, 0, perform_command, ())
schedule.run()