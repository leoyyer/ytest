#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :re.py
@说明        :
@时间        :2023/04/25 17:05:17
@作者        :Leo
@版本        :1.0
"""
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
        if not s.strip():  # 如果字符串为空或者只包含空格，则直接返回原字符串
            return s
        else:
            d = json.loads(s)
            # 处理中文
            d = {
                k.encode("latin1").decode("unicode_escape"): (
                    v.encode("latin1").decode("unicode_escape")
                    if isinstance(v, str)
                    else v
                )
                for k, v in d.items()
            }
            return d
    except (ValueError, AttributeError, TypeError):
        return s


if __name__ == "__main__":
    str_to_dict("")
