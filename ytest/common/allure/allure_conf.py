#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :allure_data.py
@说明        :
@时间        :2021/09/09 19:52:31
@作者        :Leo
@版本        :1.0
"""

import json
import allure


def allure_data(params):
    """[summary]
    在allure中,规范输出需要展示的内容
    Args:
        params ([type]): [description]
    """
    target = ""
    try:
        if isinstance(params, dict):
            if "text" in params:
                params.pop("text")
            target = json.dumps(
                params,
                sort_keys=True,
                indent=4,
                separators=(",", ":"),
                ensure_ascii=False,
            )
        else:
            data = json.loads(params)
            target = json.dumps(
                data,
                sort_keys=True,
                indent=4,
                separators=(",", ":"),
                ensure_ascii=False,
            )
    except Exception:
        target = params
    return target


def allure_step(step: str, var: str) -> None:
    """
    :param step: 步骤及附件名称
    :param var: 附件内容
    """
    var = json.loads(var)
    with allure.step(step):
        allure.attach(
            json.dumps(var, ensure_ascii=False, indent=4),
            step,
            allure.attachment_type.JSON,
        )


def allure_step_no(step: str):
    """
    无附件的操作步骤
    :param step: 步骤名称
    :return:
    """
    with allure.step(step):
        pass


def allure_title(title: str) -> None:
    """allure中显示的用例标题"""
    allure.dynamic.title(title)
