# -*- coding:utf-8 -*-
# 需要设置环境变量：NODESEEK_COOKIE，只需要 NodeSeek 的 session。

"""
cron: 23 8 * * *
new Env('NodeSeek Checkin');
"""

import os

import requests

cookie = os.getenv('NODESEEK_COOKIE')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': cookie
}


def nodeseek():
    print(headers)
    url = 'https://www.nodeseek.com/api/attendance?random=true'
    res = requests.post(url, headers=headers)
    print(res)


if __name__ == '__main__':
    nodeseek()
