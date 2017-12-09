#!/usr/bin/python2
# coding:utf8

from dataIPO import getIPOData
from tdxtrader import TdxTrader

def IPO():
    if getIPOData():
        # 有新股
        tt = TdxTrader()
        tt.prepare('account.json')
        tt.autoIPO()
        tt.close()    

def IPO2():
    if getIPOData():
        # 有新股
        tt = TdxTrader()
        tt.prepare('account2.json')
        tt.autoIPO()
        tt.close()    

if __name__ == '__main__':
    IPO2()
