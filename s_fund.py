# -*- coding:utf-8 -*-

"""
cron: 45 11,14 * * *
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
    print(fund_code)
    result = ''
    for fund in json.loads(fund_code):
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
        color = 'red'
        if float(gszzl) < 0:
            color = 'green'
        fontColor = '<font color=\"%s\">%s</font>' % (color, gszzl)
        noticeData = '%s（%s），涨跌幅：%s（%s）；\n' % (name, fundcode, fontColor, gztime)
        result += noticeData
        random_sleep()
    return result


def send_push_plus(title, content):
    token = os.getenv('PUSH_PLUS_TOKEN')
    data = {
        "token": token,
        "title": title,
        "content": content
    }
    url = 'https://www.pushplus.plus/send'
    body = json.dumps(data).encode(encoding='utf-8')
    plusHeaders = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=plusHeaders)
    pass


def random_sleep(mu=1, sigma=0.4):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    time.sleep(secs)


def start():
    if get_holiday():
        content = get_fund()
        print(content)
        send_push_plus('行情', content)
        send('行情1', content)
    pass


if __name__ == '__main__':
    start()
