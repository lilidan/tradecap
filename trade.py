# -*- coding: utf-8 -*-

import sys
import os  
import pandas as pd
import time
import json
import urllib



class trader:
    # def __init__(self):
        # self.holding = {i['stock_code']:i for i in self.user.position if i['market_value'] > 10} 
        # self.balance = self.user.balance
        # self.enable_balance = self.balance['enable_balance']
        # self.user.cancel_all()

    def get_asset():
        URL = "http://127.0.0.1:5000/asset"
        data = urllib.urlopen(URL).read()
        return data

    def get_holding():
        URL = "http://127.0.0.1:5000/holdings"
        data = urllib.urlopen(URL).read()
        return data

    def buy(self, stock, amount, price):
        TRADE_URL = "http://localhost:5000/buy?stockcode=" + stock +"&price=" + str(price) +"&amount=" + str(amount)

    def sell(self, stock, amount, price):
        TRADE_URL = "http://localhost:5000/sell?stockcode=" + stock +"&price=" + str(price) +"&amount=" + str(amount)

if __name__ == '__main__':
    t = trader()
