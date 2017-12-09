#!/usr/bin/python2
# coding:utf8

import time
import urllib2
import socket

def getIPOData():
    """
    查询今天可以申购的新股信息
    :return: 今日可申购新股列表 apply_code申购代码 price发行价格
    """

    import random
    import json
    import datetime
    import requests

    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0'
    send_headers = {
        'Host': 'xueqiu.com',
        'User-Agent': agent,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'deflate',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://xueqiu.com/hq',
        'Connection': 'keep-alive'
    }

    sj = random.randint(1000000000000, 9999999999999)
    home_page_url = 'https://xueqiu.com'
    ipo_data_url = "https://xueqiu.com/proipo/query.json?column=symbol,name,onl_subcode,onl_subbegdate,actissqty,onl" \
                   "_actissqty,onl_submaxqty,iss_price,onl_lotwiner_stpub_date,onl_lotwinrt,onl_lotwin_amount,stock_" \
                   "income&orderBy=onl_subbegdate&order=desc&stockType=&page=1&size=30&_=%s" % (str(sj))

    session = requests.session()
    session.get(home_page_url, headers=send_headers)  # 产生cookies
    ipo_response = session.post(ipo_data_url, headers=send_headers)

    json_data = json.loads(ipo_response.text)
    today_ipo = []

    for line in json_data['data']:
        # if datetime.datetime(2016, 9, 14).ctime()[:10] == line[3][:10]:
        if datetime.datetime.now().strftime('%a %b %d') == line[3][:10]:
            today_ipo.append({
                'stock_code': line[0],
                'stock_name': line[1],
                'apply_code': line[2],
                'price': line[7]
            })

    return today_ipo




if __name__ == '__main__':
    print getIPOData()

