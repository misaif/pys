# -*- coding:utf-8 -*-
# 需要设置环境变量：GLADOS_COOKIE（GLaDOS Cookie），多个用 & 分割

"""
cron: 17 7 * * *
new Env('GLaDOS Checkin');
"""

import json
import os
import random
import time
import requests

from notify import send

cookies = os.getenv('GLADOS_COOKIE')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'


def checkin():
    count = 0
    message = ''
    if cookies is None:
        print('请设置环境变量：GLADOS_COOKIE')
        return
    for cookie in cookies.split('&'):
        count += 1
        url = 'https://glados.rocks/api/user/checkin'
        payload = {'token': 'glados.network'}
        headers = {'cookie': cookie, 'user-agent': user_agent, 'content-type': 'application/json;charset=UTF-8'}
        data = requests.post(url, headers=headers, data=json.dumps(payload))
        code = data.json()['code']
        if code == 0:
            stat = '签到成功！'
        elif code == 1:
            stat = '已签到！'
        else:
            stat = 'Cookie 过期或系统异常！'
        mess = '第 ' + str(count) + ' 个账号，' + stat
        message += mess + '\n'
        random_sleep()
    send('GLaDOS Checkin', message)


def random_sleep(mu=1, sigma=0.4):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    time.sleep(secs)


if __name__ == '__main__':
    checkin()
