#!/usr/bin/env python2
# coding: utf-8

import os
import re
import time
from IPO import *
from tradeday import is_trade_day
from smallcapstock import *
from selltopstocks import *
from assetSms import *
from selector import *
from datetime import datetime, timedelta


# 调仓时间
SELL_TIME = '09:31:00'

# 调仓时间
ADJUST_TIME = '14:48:00'

# 发邮件时间
IPO_TIME2 = '11:07:06'

# 打新时间
IPO_TIME = '11:06:06'

def cal_sleep_time():
    today = time.strftime('%Y%m%d')
    
    
    time1 = datetime.strptime(today + ' ' + ADJUST_TIME, "%Y%m%d %H:%M:%S")
    time2 = datetime.strptime(today + ' ' + IPO_TIME2, "%Y%m%d %H:%M:%S")
    time3 = datetime.strptime(today + ' ' + IPO_TIME, "%Y%m%d %H:%M:%S")
    time4 = datetime.strptime(today + ' ' + SELL_TIME, "%Y%m%d %H:%M:%S")
    datetime_now =  datetime.now()
    diff1 =  (time1 - datetime_now).seconds
    diff2 =  (time2 - datetime_now).seconds
    diff3 =  (time3 - datetime_now).seconds
    diff4 =  (time4 - datetime_now).seconds

    diff1 = diff1 if diff1 >= 0 else 24 * 60 *60 + diff1
    diff2 = diff2 if diff2 >= 0 else 24 * 60 *60 + diff2
    diff3 = diff3 if diff3 >= 0 else 24 * 60 *60 + diff3
    diff4 = diff4 if diff4 >= 0 else 24 * 60 *60 + diff4

    return min(diff1,diff2, diff3,diff4)

def sleep(sleep_time):
    if sleep_time and sleep_time != -1:
        sleep_time = sleep_time - 10 if sleep_time >= 10 else 0
        print u'定时任务启动，请勿关闭窗口！！！'.encode('gbk')
        print 'Waiting time: %s ...' % str(sleep_time)
        print 'Next task run in %s ...' % (datetime.now() + timedelta(seconds=sleep_time)).strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(sleep_time)

def timer():
    sleep_time = cal_sleep_time() 
    while True:
        sleep(sleep_time)
        sleep_time = -1
        today = time.strftime('%Y%m%d')
            
        now = datetime.now().strftime('%H:%M:%S')
        if now == ADJUST_TIME:
            # 调仓
            if is_trade_day(today):
                # 如果是交易日
                scs = smallCapStock(target_num=STOCKS_NUM)
                scs.adjust()
                sleep_time = cal_sleep_time() 
            else:
                sleep_time = cal_sleep_time() 
                continue
            
        if now == IPO_TIME2:
            # 发送邮件
            if is_trade_day(today):
                # 如果是交易日
                IPO2()
                sleep_time = cal_sleep_time() 
            else:
                sleep_time = cal_sleep_time() 
                continue


        if now == IPO_TIME:
            # 打新时间
            if is_trade_day(today):
                # 如果是交易日
                IPO()
                sleep_time = cal_sleep_time() 
            else:
                sleep_time = cal_sleep_time() 
                continue


        # if now == SELL_TIME:
        #     # 打新时间
        #     if is_trade_day(today):
        #         # 如果是交易日
        #         scs = SellTopStocks(target_num=STOCKS_NUM)
        #         scs.adjust()
        #         sleep_time = cal_sleep_time() 
        #     else:
        #         sleep_time = cal_sleep_time() 
        #         continue


if __name__ == '__main__':
    timer()
    
    
