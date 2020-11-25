# -*- coding:utf-8 -*-
import time
from datetime import datetime

from log import logger


class Timer(object):

    def __init__(self, buy_time, sleep_interval=0.01):

        # '2018-09-28 22:45:50.000'
        self.buy_time = datetime.strptime(buy_time, "%Y-%m-%d %H:%M:%S.%f")
        self.sleep_interval = sleep_interval

    def start(self):
        logger.info('正在等待到达设定时间:%s' % self.buy_time)
        now_time = datetime.now
        while True:
            if now_time() >= self.buy_time:
                logger.info('时间到达，开始执行...%s '%(datetime.now()))
                break
            else:
                # t0=time.time()
                time.sleep(self.sleep_interval)
                # t1=time.time()
                # logger.info('interval:%s'%(round(t1-t0,2)))
