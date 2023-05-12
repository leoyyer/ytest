#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :06.py
@说明        :
@时间        :2023/05/09 10:31:20
@作者        :Leo
@版本        :1.0
'''

import json
import re

# dict = {'from': '2023-05-09 00:00:00', 'to': '2023-05-09 10:30:25'}
# dd = json.dumps(dict)
# print(type(dd))

# _now_assert_data = str({'type': 'response_body', 'text': 'code=2000;msg=成功'})
# _assert_list = list(set(re.findall(r"body.(.*?)(?=(,|}))", _now_assert_data)))
# print(_assert_list)

exp = '{"type":"response_body","text":"code=2000;msg=成功"};{"type":"length_equals","text":"res=body.data.envs","len":1 }'

pattern = r'\{.*?\}'



# 使用正则表达式解析字符串，得到匹配的结果列表
# match_list = re.findall(pattern, exp)
# for i in match_list:
#     match_dict = json.loads(i)
#     print(match_dict)
    
# data = '{"type":"length_equals","text":{"res":"body.data.envs"}'
# match_dict = json.loads(data)
# print(match_dict)
# 报错:json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 56 (char 55)
import jsonpath
body = {'status_code': 200, 'body': {'code': 2000, 'msg': '成功', 'data': [{'customer_id': '', 'customer_name': '天眼内置', 'envs': [{'code': 'prod', 'name': '生产环境', 'enable': 1, 'mks_env_code': '', 'mks_env_tag': 'prod', 'source': 1, 'customer_id': '', 'customer_name': ''}]}]}, 'text': '{"code":2000,"msg":"成功","data":[{"customer_id":"","customer_name":"天眼内置","envs":[{"code":"prod","name":"生产环境","enable":1,"mks_env_code":"","mks_env_tag":"prod","source":1,"customer_id":"","customer_name":""}]}]}', 'time_consuming': 295.52, 'time_total': 0.29552}
cc = jsonpath.jsonpath(body['body'], '$.data')
print(cc)
print(len(cc))
