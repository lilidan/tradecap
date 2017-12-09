#!/usr/bin/python
# coding:utf8
# return all stocks information include price and voloum, excluding ST and risk notification stocks

import json
import pandas as pd
import easyquotation

BLACK_LIST = ["000033","300372"]

def get_prices():
    qq = easyquotation.use("qq")
    df = pd.DataFrame(qq.all)
    df = df.T
    to_drop = list(df.columns)
    to_drop.remove('ask1')
    to_drop.remove("bid1")
    to_drop.remove("ask5")
    to_drop.remove("bid5")
    to_drop.remove("now")
    to_drop.remove('name')
    to_drop.remove(u"流通市值")
    to_drop.remove(u'涨停价')
    to_drop.remove(u'跌停价')
    to_drop.remove('unknown')
    to_drop.remove('volume')
    to_drop.remove('low')
    df = df.drop(pd.Index(to_drop),1)
    df.columns = ["ask1","ask5","bid1","bid5","low","name","now","unknown","volume","cap","highlimit","lowlimit"]
    df = df[~df["name"].str.contains("S")]
    df = df[df.index.str.slice(0,1).isin(["0","3","6"]) == True]
    df = df[df.index.isin(BLACK_LIST) == False]
    df = df.sort_values(["cap"],ascending=True,inplace=False)
    df = df[:2000]

    return df

def select():
    result = get_prices()
    return result

if __name__ == '__main__':
    print select(read_cache=False)
