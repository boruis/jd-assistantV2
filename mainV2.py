#!/usr/bin/env python
# -*- coding:utf-8 -*-
from jd_assistant import Assistant
import random

import requests
import datetime,json,time
import os
if os.name == 'nt':
    import win32api
# import sys
# sys.path.insert(0,'\\Library\\bin')
# sys.path.append('\\Library\\bin')
# print(sys.path)
"""
python area_id/arget_area_id.py 获取区域ID
"""
def setSystemTime():
    url = 'https://a.jd.com//ajax/queryServerData.html'
    session = requests.session()
    # get server time
    t0 = datetime.datetime.now()
    ret = session.get(url).text
    t1 = datetime.datetime.now()
    t_now = time.time()
    js = json.loads(ret)
    t = float(js["serverTime"]) / 1000
    dt = datetime.datetime.fromtimestamp(t) + ((t1 - t0) / 2)
    print("jdT:%s Lt:%s dT:%s diff:%s"%(datetime.datetime.fromtimestamp(t),t1,dt,round(t-t_now,2)))
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(time.mktime(dt.timetuple()))
    msec = dt.microsecond / 1000
    # if os.name == 'nt':
    # win32api.SetSystemTime(tm_year, tm_mon, tm_wday, tm_mday, tm_hour, tm_min, tm_sec, int(msec))
    '''
    ret2=session.get(url).text
    dttime = float(json.loads(ret)["serverTime"]) / 1000
    dt2 = datetime.datetime.fromtimestamp(dttime)
    tnow = time.time()
    print("jd:%s : %s now:%s  %s diff:%s   "%(dt2,dttime,datetime.datetime.fromtimestamp(tnow),tnow,round(dttime-tnow,2)))
    '''
# setSystemTime()

from timer import Timer
dt = time.time() 
buy_time = str(datetime.datetime.fromtimestamp(dt+2))
# buy_time = '2020-11-25 13:54:01.0000'
print("Test now:    %s   buy_time:%s"%(datetime.datetime.fromtimestamp(dt),buy_time))
t = Timer(buy_time=buy_time)
t.start()

if __name__ == '__main__':
    """
    重要提示：此处为示例代码之一，请移步下面的链接查看使用教程👇
    https://github.com/tychxn/jd-assistant/wiki/1.-%E4%BA%AC%E4%B8%9C%E6%8A%A2%E8%B4%AD%E5%8A%A9%E6%89%8B%E7%94%A8%E6%B3%95
    """
    #area = '19_1607_4773'  # 区域id
    asst = Assistant()  # 初始化
    model_type = input("请输入购买类型(1.定时预约抢购 2.正常有货购买 3.正常定时购买)：")
    asst.login_by_QRcode()  # 扫码登陆
    #asst.get_single_item_stock(100006394713,1,'19_1607_4773')
    # 获取参数信息  100016578654    100009514841
    interval = 0.1  #预约间隔时间
    retry = 5  #重试次数
    if model_type == '1':
        print("定时预约抢购...")
        sku_id = input("请输入一个sku_id:")
        asst.print_item_info(sku_id)
        reserve_info = asst.get_reserve_info(sku_id)
        reserve_time = reserve_info.get("yueStime")
        buy_time = reserve_info.get("qiangStime")
        print("预约时间:",reserve_time)
        print("抢购时间:",buy_time)
        # 开始预约
        if reserve_time :
            asst.make_reserve(sku_id, reserve_time + '.000')
        else:
            print('获取预约时间失败')
        # 开始抢购
        if buy_time :
            rand_msecond = random.randint(1,9) * 1000
            buy_time = buy_time + '.000'
            #buy_time = buy_time + "." + str(rand_msecond)
        else:
            print('获取抢购时间失败')
            buy_time = input("请输入抢购时间(2020-03-04 00:59:59.000):")
        #asst.exec_reserve_seckill_by_time(sku_id=sku_id,buy_time=time, retry=10, interval=1,num=1)
        asst.exec_seckill_by_time(sku_ids=sku_id,buy_time=buy_time, retry=retry, interval=interval,num=1)
    elif model_type == '2':
        print("正常有货购买...")
        sku_ids = input("请输入一个或多个sku_id:")
        area = input("请输入area_id:")
        asst.buy_item_in_stock(sku_ids=sku_ids, area=area, wait_all=False, stock_interval=5)
    elif model_type == '3':
        print("正常定时购买...")
        sku_ids = input("请输入一个或多个sku_id:")
        buy_time = input("请输入定时购买时间(2020-03-04 00:59:59.000):")
        asst.clear_cart()       # 清空购物车（可选）
        asst.add_item_to_cart(sku_ids=sku_ids)  # 根据商品id添加购物车（可选）
        asst.submit_order_by_time(buy_time=buy_time, retry=retry, interval=interval)  # 定时提交订单
