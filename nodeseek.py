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
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/119.0.0.0',
    'Cookie': cookie
}


def nodeseek():
    print(headers)
    url = 'https://www.nodeseek.com/api/attendance?random=true'
    res = requests.post(url, headers=headers)
    print(res)


if __name__ == '__main__':
    nodeseek()
