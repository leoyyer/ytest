#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :test01.py
@说明        :
@时间        :2023/05/04 14:51:26
@作者        :Leo
@版本        :1.0
'''
import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_path)
import pytest
from utils.logger.logger import MyLog
from common.control.read_xlsx import ReadXlsData
from common.conf.conf import Config


log = MyLog(logger_name=__name__)

CASE_DETAIL = {}

def get_case_detail(filename: str, conf = None):
    excel = ReadXlsData(filename)
    case_detail = excel.get_case_data()
    conf = Config(case_detail['project'],conf)
    env = conf.conf_path
    CASE_DETAIL.update({"case_detail":case_detail})
    CASE_DETAIL.update({"env":env})
    return CASE_DETAIL



if __name__ == '__main__':
    get_case_detail('data/fast/suite/fast_auto_product_screen.xlsx')
    print('CASE_DETAIL',CASE_DETAIL)
    pytest.main(['-s', '-x', "-o", "log_cli=true", "-o", "log_cli_level=INFO", r'ytest/utils/case/default_case.py'])