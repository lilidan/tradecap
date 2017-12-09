#!/usr/bin/python2
#coding: utf-8 

from __future__ import division

import time
from selector import select
from trader import trader
import pandas as pd

# 交易 溢价
PREMIUM = 1.02

LIMIT_DOWN = -1
LIMIT_UP = -2
STOCKS_NUM = 8


class smallCapStock:
    def __init__(self, target_num=10, clear_all=False):
        ''' 当日全部股票 '''
        self.clear_all = clear_all
        if self.clear_all:
            raw_input(u'请按回车确定清仓,否则退出程序!!!'.encode('gbk'))
        self.target_num = target_num
        self.trader = trader()

    def adjust(self):
        # 持仓股票
        holding_stocks = self.trader.holding.keys()

        # 目标股票决策
        target_df = self.target_stocks_decision(holding_stocks)
        target_stocks = list(target_df.index)

        print target_df

        # 清仓
        if self.clear_all:
            self.sell_out([i for i in holding_stocks])
            return 
        
        stocks_log = str(target_stocks) + "---S---" +  str([i for i in holding_stocks if i not in target_stocks]) + "--B--" + str([i for i in target_stocks if i not in holding_stocks])

        # 卖出
        sell_amt = self.sell_out([i for i in holding_stocks if i not in target_stocks])
        # 卖出后等待5秒
        time.sleep(5)
        # 开仓
        self.buy_in([i for i in target_stocks if i not in holding_stocks], sell_amt)

    def sell_out(self, stocks):
        ''' 清仓
        '''
        amt = 0
        #print("SELL:"+stocks)
        for stock in stocks:
            amount = self.trader.holding.get(stock).get('enable_amount') or 0
            if amount > 100:
                # amount 单位是股票数，不是手数
                decision = self.trade_price_decision(stock, amount, 'sell',len(stocks) >= 2)
                trade_price = decision[1]
                if int(trade_price) != 0:
                    #print amount,stock,trade_price
                    self.trader.sell(str(stock), int(amount), trade_price)
                    # 假设成功卖出,扣除印花税
                    amt += int(amount) * trade_price * 0.999
        return amt

    def buy_in(self, stocks, sell_amt):
        ''' 开仓 
        '''
        #print("BUY:"+stocks)
        if len(stocks) == 0:
            return
        # 重新获取账户 可用余额
        # enable_balance = self.trader.user.balance.get('enable_balance')
        self.balance = self.trader.user.balance
        self.enable_balance = self.balance['enable_balance']
        enable_balance = self.enable_balance + sell_amt
        # 每支调仓股票可用余额
        each_enable_balance = enable_balance/len(stocks)
        #print self.trader.balance
        for stock in stocks[:-1]:
            amount, trade_price = self.trade_price_decision(stock, each_enable_balance, 'buy',len(stocks) >= 2)
            if amount>=100 and int(trade_price) != 0:
                #print amount,stock,trade_price
                self.trader.buy(str(stock), amount, trade_price)
                total = amount * trade_price + 5
                enable_balance = enable_balance - total

        last_stock = stocks[-1]
        amount, trade_price = self.trade_price_decision(last_stock, enable_balance, 'buy',len(stocks) >= 2)
        if amount>=100 and int(trade_price) != 0:
            self.trader.buy(str(last_stock), amount, trade_price)

    def target_stocks_decision(self, holding_stocks):
        ''' 1. 考虑目标股票中存在涨停或者跌停的情况
            如果持仓中没有这些目标股票，则跳过，顺序替补次小市值股票。如果有，则持仓
            2. 考虑持仓股票中有停牌的情况
        '''

        df = select()
        self.df = df
        holding = (df.index.isin(holding_stocks) == True)
        lowlimit = (df["now"] == df["lowlimit"]) #跌停
        unknown = (df["unknown"] != "") #未知状况
        novolume = (df["volume"] == 0) #没有成交
        highlimit = (df["low"] == df["highlimit"]) #一字板
        remain_df = df[holding & (lowlimit | unknown | novolume | highlimit)]
        remain_count = len(remain_df)
        target_df = df[df.index.isin(remain_df.index) == False]
        target_df = target_df[target_df["now"] < target_df["highlimit"]]
        target_df = target_df[target_df["volume"] > 0]
        target_df = target_df[target_df["unknown"] == ""]
        target_df = target_df[:self.target_num - remain_count]
        target_df = pd.concat([target_df,remain_df])

        return target_df

    def trade_price_decision(self, stock, value, direction, isForce = False):
        '''交易价格决策, 按十档委托数量定价
           direction: 交易方向sell 或 buy
           value: 交易方向是sell时是可用仓位, buy是可用现金
        '''
        if direction == 'sell':
            '''卖出'''
            return None, self.df["bid5"][stock] if isForce else self.df["bid1"][stock]
        else:
            '''买入'''
            # 跌停 或正常交易
            price = self.df["ask1"][stock]
            now_price = self.df["now"][stock]
            if price > now_price * 1.005:
                price = int(now_price * 1.005 * 100.0) / 100.0
            if isForce:
                price = self.df["ask5"][stock]
            amount = int(value/price/100) * 100
            return amount, price

if __name__ == '__main__':
    import sys
    clear = False
    if len(sys.argv) == 2:
        clear = True if sys.argv[1] == 'True' else False
    scs = smallCapStock(target_num=STOCKS_NUM, clear_all=clear)
    scs.adjust()
    #print scs.trade_price_decision(i['code'], 100000, 'buy')
