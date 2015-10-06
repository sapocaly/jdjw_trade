#! /usr/bin/env python
# coding=utf-8


import utils.PathHelper

import time
import sched
import datetime
import threading
import mini_fetcher
import utils.LogConstant as LogConstant

schedule = sched.scheduler(time.time, time.sleep)

logger = LogConstant.FETCH_DIGEST_LOGGER


def perform_command():
    ##do something
    logger.info('starting python')
    thread = threading.Thread(target=mini_fetcher.run)
    thread.start()
    now = datetime.datetime.now()
    delta = (1100000 - now.microsecond) / 1000000.0
    schedule.enter(delta, 0, perform_command, ())


now = datetime.datetime.now()
delta = (1100000 - now.microsecond) / 1000000.0
schedule.enter(delta, 0, perform_command, ())
schedule.run()
