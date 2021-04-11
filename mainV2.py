#!/usr/bin/env python
# -*- coding:utf-8 -*-
from jd_assistant import Assistant
import random

import requests
import datetime
import json
import time
import os
# if os.name == 'nt':
#     import win32api
from log import logger
import socket
import urllib
from timer import Timer, getTimeDurationDate,toTimeStamp
# import sys
# sys.path.insert(0,'\\Library\\bin')
# sys.path.append('\\Library\\bin')
# print(sys.path)
"""
python area_id/arget_area_id.py 获取区域ID
https://api.m.jd.com/client.action?functionId=queryMaterialAdverts&client=wh5\
&user-agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36
"""


def getRemoteTimeDiff():
    hostname = 'a.jd.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    headers['Host'] = hostname
    # url = 'https://a.jd.com//ajax/queryServerData.html'
    dns_start = time.time()
    ip_address = socket.gethostbyname(hostname)
    dns_end = time.time()
    # url = 'https://%s//ajax/queryServerData.html' % hostname
    url = 'http://%s//ajax/queryServerData.html' % ip_address
    # url = 'https://%s/' % ip_address
    req = urllib.request.Request(url, headers=headers)
    # req.add_header('Host', hostname)

    handshake_start = time.time()
    stream = urllib.request.urlopen(req)
    handshake_end = time.time()

    data_start = time.time()
    ret = (stream.read())
    data_end = time.time()


    DNS_time = (dns_end - dns_start) * 1000
    HTTP_handshake_time = (handshake_end - handshake_start) * 1000
    HTTP_data_time = (data_end - data_start) * 1000
    totalSystem = (data_end - dns_start) * 1000
    All_req=DNS_time+HTTP_handshake_time+HTTP_data_time

    data_length = len(ret)
    js = json.loads(ret)
    t = float(js["serverTime"]) / 1000

    # time_duration = HTTP_data_time / 1000
    # nettime2 =  
    nettime = HTTP_data_time
    time_duration = round(t - data_end,4)
    # countNet = round(time_duration - nettime / 2, 4)
    countNet = round(time_duration - nettime , 4)

    print('DNS time            = %.4f ms' % (DNS_time))
    print('HTTP handshake time = %.4f ms' % (HTTP_handshake_time))
    print('HTTP data time      = %.4f ms' % (HTTP_data_time))
    print('Data received       = %s bytes' % data_length)
    print('totalSystem         = %.4f ms  All_req:%.4f ms diff:%.4f' % (totalSystem,All_req,totalSystem-All_req))
    logger.info("jd:%.4f HTTP_data_time:%.4f time_duration:%04f countNet:%0.4f " % (
         All_req, HTTP_data_time, time_duration, countNet))

def getSystemTimeduration():
    # get server time

    url = 'https://a.jd.com//ajax/queryServerData.html'
    session = requests.session()
    t0_s = time.time()  # local host time
    r = session.get(url)
    ret = r.text
    t_now = time.time()

    t0 = datetime.datetime.fromtimestamp(t0_s)
    t1 = datetime.datetime.fromtimestamp(t_now)

    js = json.loads(ret)
    t = float(js["serverTime"]) / 1000  # remote Host time
    # remote time + nettime/2 ->now dttime
    dt = datetime.datetime.fromtimestamp(t) + ((t1 - t0) / 2)
    nettime2 = t_now - t0_s  # total url and system time
    nettime = r.elapsed.total_seconds()  # request total time
    time_duration = round(t - t_now, 4)  # remote time - local time
    # countNet = round(time_duration - nettime / 2, 4)
    countNet = round(time_duration - nettime , 4)
    logger.info("t0:%s t1:%s elapsed:%s nettime2:%0.4f" %
                (t0, t1, nettime, nettime2))
    logger.info("jd:%s dT:%s diff:%s countNet:%0.4f " % (
        datetime.datetime.fromtimestamp(t), dt, time_duration, countNet))
    # tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(time.mktime(dt.timetuple()))
    # msec = dt.microsecond / 1000
    # if os.name == 'nt':
    #     win32api.SetSystemTime(tm_year, tm_mon, tm_wday, tm_mday, tm_hour, tm_min, tm_sec, int(msec))

    return time_duration
    '''
    ret2=session.get(url).text
    dttime = float(json.loads(ret)["serverTime"]) / 1000
    dt2 =   .datetime.fromtimestamp(dttime)
    tnow = time.time()
    print("jd:%s : %s now:%s  %s diff:%s   "%(dt2,dttime,datetime.datetime.fromtimestamp(tnow),tnow,round(dttime-tnow,2)))
    '''


#getRemoteTimeDiff()
#time_duration = getSystemTimeduration()
time_duration = 0


dt = time.time()
buy_time = str(datetime.datetime.fromtimestamp(dt + 2 - time_duration))
buy_time1 = getTimeDurationDate(buy_time, time_duration)
# buy_time1 = getTimeDurationDate(buy_time, -1.0)

# buy_time = str(datetime.datetime.fromtimestamp(dt+2))
# buy_time = '2020-11-25 13:54:01.0000'

logger.info("Test now:   %s  buy_time:%s time_duration:%s fixTime:%s",
            datetime.datetime.fromtimestamp(dt), buy_time, time_duration,buy_time1)
t = Timer(buy_time=buy_time, sleep_interval=0.01)
t.start()

if __name__ == '__main__':
    """
    重要提示：此处为示例代码之一，请移步下面的链接查看使用教程👇
    https://github.com/tychxn/jd-assistant/wiki/1.-%E4%BA%AC%E4%B8%9C%E6%8A%A2%E8%B4%AD%E5%8A%A9%E6%89%8B%E7%94%A8%E6%B3%95
    """
    # area = '19_1607_4773'  # 区域id
    asst = Assistant()  # 初始化

    if not asst.sku_id:
        sku_id = '100012043978'  # (飞天)
    else:
        sku_id = asst.sku_id
    # sku_id = '100001324422'   #(Test)
    # model_type = '2'
    if not asst.model_type:
        model_type = '1'
    else:
        model_type = asst.model_type
    # area = '1_72_55677'   #area id
    if not asst.area:
        area = '1_72_55677'  # area id
        # area = '1_2802_54746'  # area id
    else:
        area = asst.area

    if not asst.loopinterval:
        loopinterval = 0.1  # 预约间隔时间
    else:
        loopinterval = asst.loopinterval

    if not asst.retry:
        retry = 3  # 没有抢到,重试次数
    else:
        retry = asst.retry
    # if not asst.retryinterval:
    #     retryinterval = 0.05 #链接获取失败,重试间隔
    # else:
    #     retryinterval = asst.loopinterval
    
    if not model_type:
        model_type = input("请输入购买类型(1.定时预约抢购 2.正常有货购买 3.正常定时购买)：")
    asst.login_by_QRcode()  # 扫码登陆
    # asst.get_single_item_stock(100006394713,1,'19_1607_4773')
    # 获取参数信息  100016578654    100009514841   100012043978 (飞天)
    # 100015521004 (七彩3080)

    if model_type == '1':
        print("定时预约抢购...")
        if not sku_id:
            sku_id = input("请输入一个sku_id:")
        else:
            logger.info("定时预约sku_id:%s"%(sku_id))
        asst.print_item_info(sku_id)
        reserve_info = asst.get_reserve_info(sku_id)
        reserve_time = reserve_info.get("yueStime")
        buy_time_init = reserve_info.get("qiangStime")
        logger.info("buy_time:%s"%(buy_time_init))
        # if sku_id == '100012043978':
        #     buy_time = getTimeDurationDate(buy_time_init, -0.9103)
        # else:
        #     buy_time = getTimeDurationDate(buy_time_init, time_duration)
        buy_time = getTimeDurationDate(buy_time_init, time_duration)

        logger.info("预约时间:%s", reserve_time)
        logger.info("抢购时间:%s fix:%s" % (buy_time_init, buy_time))
        # 开始预约
        if reserve_time:
            asst.make_reserve(sku_id, reserve_time + '.000')
        else:
            print('获取预约时间失败')
        # 开始抢购
        if buy_time is not None:
            rand_msecond = random.randint(1, 9) * 1000
            # buy_time = buy_time + '.000'
            # buy_time = buy_time
            #buy_time = buy_time + "." + str(rand_msecond)
        else:
            print('获取抢购时间失败')
            buy_time = input("请输入抢购时间(2020-03-04 00:59:59.000):")
        #asst.exec_reserve_seckill_by_time(sku_id=sku_id,buy_time=time, retry=10, interval=1,num=1)
        if toTimeStamp(buy_time) - time.time() > 100:
            asst.exec_seckill_by_time(
                sku_ids=sku_id, buy_time=buy_time, retry=retry, interval=loopinterval, num=1)
        else:
            logger.info("已过时:buy_time:%s now:%s"%(buy_time,datetime.datetime.now()))
            
    elif model_type == '2':
        print("正常有货购买...")
        if not sku_id:
            sku_id = input("请输入一个或多个sku_id:")
        if not area:
            area = input("请输入area_id:")
        asst.buy_item_in_stock(sku_ids=sku_id, area=area,
                               wait_all=False, stock_interval=5)
    elif model_type == '3':
        print("正常定时购买...")
        sku_ids = input("请输入一个或多个sku_id:")
        buy_time = input("请输入定时购买时间(2020-03-04 00:59:59.000):")
        asst.clear_cart()       # 清空购物车（可选）
        asst.add_item_to_cart(sku_ids=sku_ids)  # 根据商品id添加购物车（可选）
        asst.submit_order_by_time(
            buy_time=buy_time, retry=retry, interval=loopinterval)  # 定时提交订单
