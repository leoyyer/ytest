#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :fast.py
@说明        :
@时间        :2023/04/25 10:06:32
@作者        :Leo
@版本        :1.0
'''

import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from datetime import datetime, timedelta
import requests
import json


def get_token(url, username, password):
    """_summary_
    获取token
    Args:
        url (_type_): _description_
        username (_type_): _description_
        password (_type_): _description_

    Returns:
        _type_: _description_
    """
    headers = {
        'authority': 'mks-test.mypaas.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-current-module': 'ldaplogin',
        'x-fast-trace-id': 'fast-254d25399028a40-b9a4004f3f-6847475f'
    }
    data = {
        'account': username,
        'password': "F&4&SEd^$G"
    }
    # return 66666
    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        token = response.json()['data']['token']
        return token
    else:
        response.raise_for_status()


def generate_overview_time_range(space=None,page=None):
    """
    overview模块使用
    """
    now = datetime.now()
    today = datetime(now.year, now.month, now.day, 0, 0, 0)
    data = {"from": str(today), "to": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),}
    if page:
        data.update({"page_index": int(page), "page_size": "5"})
    if space:
        data.update({"space": int(space)})
    return json.dumps(data)


def get_data(data):
    pass


def generate_time_range(interval, num=None):
    orders = ["", "error_num desc", "error_api_num desc", "crash_num desc", "slow_page_num desc", "slow_api_num desc","slow_sql_num desc"]
    data = {"from": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "to": (datetime.now() + timedelta(days=int(interval))).replace(hour=23, minute=59, second=59).strftime("%Y-%m-%d %H:%M:%S")}
    if num:
        data.update({"page_index": "1", "page_size": "100", "orders": orders[int(num)]})
    return json.dumps(data)


def update_data_time(data):
    data = '{"type":"func","func":"${update_data_time(data={"page_index": "1", "page_size": "20", "from": "2023-04-14 00:00:00", "to": "2023-04-20 23:59:59", "filters": "[{\"relations\":[{\"field\":\"app\",\"operator\":\"eq\",\"values\":[]},{\"field\":\"app_version\",\"operator\":\"in\",\"values\":[]},{\"field\":\"os_version\",\"operator\":\"multiIn\",\"values\":[]},{\"field\":\"plugin_version\",\"operator\":\"multiIn\",\"values\":[]},{\"field\":\"is_crash_killer\",\"operator\":\"eq\",\"values\":[0]}],\"relation_type\":\"and\"}]", "orders": "[{\"field\":\"crash_count\",\"way\":\"desc\"}]", "status": "-1"})}","key":"new_param"}'
    now = datetime.now()
    data['from'] = str(datetime(now.year, now.month, now.day, 0, 0, 0))
    data['to'] = str(datetime(now.year, now.month, now.day, 23, 59, 59))
    return json.dumps(data)


def get_num_data(num):
    return num


if __name__ == '__main__':
    test = generate_time_range(interval=7)
    # test = update_data_time()
    test = get_token("https://mks-test.mypaas.com/auth-api/v2/user/login", "pengda01", "123456")
    print(test)