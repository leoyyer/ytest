#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :extracts.py
@说明        :
@时间        :2023/05/10 18:01:14
@作者        :Leo
@版本        :1.0
"""

from ytest.common.Logger import logger
import jsonpath


def extract(response, extract_param, global_variable):
    """
    参数提取,更新到全局变量
    """
    if not response:
        raise ValueError("无效的响应体")
    if len(extract_param):
        for extract in extract_param:
            _extract = {i.split("=")[0]: i.split("=")[1] for i in extract.split(";")}
            value = next(iter(_extract.values()))
            res = jsonpath.jsonpath(response, f"$.{value}")
            global_variable.update({next(iter(_extract.keys())): res[0]})
    logger.info(f"[全局变量列表更新] >>> \n{global_variable}")
