#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 14:38:25 2022

@author: jacob
"""

from fake_useragent import UserAgent
import requests
import time
from requests.exceptions import ReadTimeout
import pandas as pd


def generate_random_header():
    ua = UserAgent()
    user_agent = ua.random
    header={'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': user_agent}
    return header


def find_best_session():

    for i in range(10):
        try:
            # print('獲取新的Session 第', i, '回合')
            headers  = generate_random_header()
            ses = requests.Session()
            ses.get('https://www.twse.com.tw/zh/', headers=headers, timeout=10)
            ses.headers.update(headers)
            # print('成功！')
            return ses
        except (ConnectionError, ReadTimeout) as error:
            # print(error)
            # print('失敗，10秒後重試')
            time.sleep(10)

    print('IP已經封鎖')
    print("手機  ：開啟飛航模式，再關閉，即可獲得新的IP")
    print("數據機：關閉然後重新打開數據機的電源")



ses = None
def requests_get(*args1, **args2):

    # get current session
    global ses
    if ses == None:
        ses = find_best_session()

    # download data
    i = 3
    while i >= 0:
        try:
            return ses.get(*args1, timeout=10, **args2)
        except (ConnectionError, ReadTimeout) as error:
            time.sleep(60)
            ses = find_best_session()

        i -= 1
    return pd.DataFrame()




