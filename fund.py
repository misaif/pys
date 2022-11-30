# -*- coding:utf-8 -*-
# 需要设置环境变量：FUND_CODE（基金代码），多个用英文逗号分割

"""
cron: 45 11,14,15 * * *
new Env('基金');
"""

import json
import os
import random
import time

import requests as requests

from notify import send

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


def get_holiday():
    result = False
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    url = 'https://timor.tech/api/holiday/info/' + date
    resp = requests.get(url, headers=headers).json()
    if resp['code'] == 0:
        # 节假日类型，分别表示：0 工作日、1 周末、2 节日、3 调休
        if resp['type']['type'] == 0:
            result = True
    return result


def get_fund():
    fund_code = os.getenv('FUND_CODE')
    result = ''
    for fund in fund_code.split(','):
        millis = int(round(time.time() * 1000))
        url = 'https://fundgz.1234567.com.cn/js/%s.js?rt=%d' % (fund, millis)
        resp = requests.get(url, headers=headers).text
        data = json.loads(resp[8:-2])
        # 基金代码
        fundcode = data['fundcode']
        # 基金名称
        name = data['name']
        # 估算增值率/日涨跌幅
        gszzl = data['gszzl']
        # 估值时间
        gztime = data['gztime']
        stat = '&uarr;'
        if float(gszzl) < 0:
            stat = '&darr;'
        noticeData = '%s (%s)\n涨跌幅: %s %s (%s)\n\n' % (name, fundcode, gszzl, stat, gztime)
        result += noticeData
        random_sleep()
    return result


def random_sleep(mu=1, sigma=0.4):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    time.sleep(secs)


def start():
    if get_holiday():
        content = get_fund()
        send('行情', content)
    pass


if __name__ == '__main__':
    start()
