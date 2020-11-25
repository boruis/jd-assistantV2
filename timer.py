# -*- coding:utf-8 -*-
import time
from datetime import datetime

from log import logger


# get now timeString or timeStamp
# 获取当前时间字符串或时间戳（都可精确到微秒）
def getTime(needFormat=0, formatMS=True):
    if needFormat != 0:
        return datetime.now().strftime(f'%Y-%m-%d %H:%M:%S{r".%f" if formatMS else ""}')
    else:
        ft = time.time()
        return (ft if formatMS else int(ft))


# timeString to timeStamp
# 时间字符串转时间戳（有无微秒都可）
def toTimeStamp(timeString):
    if '.' not in timeString: getMS=False
    else: getMS=True
    timeTuple = datetime.strptime(timeString, f'%Y-%m-%d %H:%M:%S{r".%f" if getMS else ""}')
    ft = float(f'{str(int(time.mktime(timeTuple.timetuple())))}'+(f'.{timeTuple.microsecond}' if getMS else ''))
    return (ft if getMS else int(ft))


def getTimeDurationDate(timeString,Duration):
    #抢购时间修正为主机时间
    dT =  toTimeStamp(timeString) - Duration
    return str(datetime.fromtimestamp(dT))
# timeStamp to timeString
# 时间戳转时间字符串
def toTimeString(timeStamp):
    if type(timeStamp) == int: getMS=False
    else: getMS=True
    timeTuple = datetime.utcfromtimestamp(timeStamp+8*3600)
    return timeTuple.strftime(f'%Y-%m-%d %H:%M:%S{r".%f" if getMS else ""}')



class Timer(object):

    def __init__(self, buy_time, sleep_interval=0.1):

        # '2018-09-28 22:45:50.000'
        self.buy_time = datetime.strptime(buy_time, "%Y-%m-%d %H:%M:%S.%f")
        self.buy_timeStamp = toTimeStamp(buy_time)
        self.sleep_interval = sleep_interval

    def start(self):
        logger.info('正在等待到达设定时间:%s' % self.buy_time)
        # now_time = datetime.now
        now_time = time.time
        while True:
            t0 = now_time()
            dt = datetime.fromtimestamp(t0)
            if dt >= self.buy_time:
                # logger.info('%s时间%s，执行...%s '%(self.buy_time,dt,datetime.now()))
                logger.info('时间到达%s，开始执行...%0.4f '%(dt,time.time()-self.buy_timeStamp))
                break
            else:
                time.sleep(self.sleep_interval)
                # t1=time.time()
                # logger.info('interval:%s'%(round(t1-t0,2)))


'''
时间小工具函数，方便进行时间处理
@author: PurePeace
@time: 2020年2月10日 02:42:55
'''

