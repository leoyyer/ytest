#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :re.py
@说明        :
@时间        :2023/04/25 17:05:17
@作者        :Leo
@版本        :1.0
'''
import json


def resolve_vars(data, var_dict):
    """
    递归处理数据中的变量，用全局变量中的对应值替换
    """
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = resolve_vars(v, var_dict)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = resolve_vars(data[i], var_dict)
    elif isinstance(data, str):
        for var_name in var_dict:
            if f"${{{var_name}}}" in data:
                data = data.replace(f"${{{var_name}}}", str(var_dict[var_name]))
    return data


def str_to_dict(s):
    """判断字符串是否能转换为字典,可以则返回字典,不可以则返回字符串"""
    try:
        d = json.loads(s)
        # 处理中文
        d = {k.encode('latin1').decode('unicode_escape'): v.encode('latin1').decode('unicode_escape') if isinstance(v, str) else v for k, v in d.items()}
        return d
    except ValueError:
        return s



if __name__ == '__main__':
    # data = [
    # {"type":"mysql","database":"api_test_starship_branch","sql":"select id as feature_id from feature where name = '${feature_name}'","key":"feature_id"},
    # {"account": "${username}", "password": "${password}", "auto_login": 0},
    # "/authapi/user/login/${username}/123",
    # {"filters": "[{\"relations\":[{\"field\":\"${username}\",\"operator\":\"eq\",\"values\":[\"fast-app\"]}],\"relation_type\":\"and\"}]", "from": "2023-03-22 00:00:00", "to": "2023-04-20 23:59:59", "app_crash_fingerprint_hash": "0CE717D3F8E57962EAFEB17803F369D9", "app": "fast-app", "view_type": "3", "field_names": "app_version,app_hotupdate_version", "page_size": "100", "page_index": "1"}
    # ]
    data = '${now_space}'
    variables = {'username': 'pengda01', 'password': '123456.0', 'url': 'https://mks-test.mypaas.com/auth-api/v2/user/login', 'now': {'from': '2023-05-08 00:00:00', 'to': '2023-05-08 17:28:40'}, 'token': 66666, 'id': 'id', 'now_page': {'from': '2023-05-08 00:00:00', 'to': '2023-05-08 17:28:40', 'page_index': 1, 'page_size': '5'}, 'feature_id': [{'id': 574252882044391424}, {'id': 574260075980394496}], 'feature_id_2': [{'id': 574252882044391424}, {'id': 574260075980394496}], 'now_space': {'from': '2023-05-08 00:00:00', 'to': '2023-05-08 17:28:41', 'space': 3600}}
    # variables = {'username': 'pengda01', 'password': 123456.0, 'url': 'https://mks-test.mypaas.com/auth-api/v2/user/login', 'now': None, 'token': '2077c7ed5a0bb7d9d19dc8503d33e4c0be949d9f', 'new_bee': None}
    result = resolve_vars(data, variables)
    print(result)
    