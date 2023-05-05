#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_path)
import pytest
from utils.logger.logger import MyLog
import allure
from utils.case.case_run import CASE_DETAIL,get_case_detail


log = MyLog(logger_name=__name__)

import pytest
import allure

class TestSuite(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.case_detail = get_case_detail(self.filepath)
        self.case_list = self.case_detail['case_detail']['case_list']
        self.ids = self.case_detail['case_detail']['base']['case_len']
        self.ids = [0, 1, 2, 3, 4, 5, 6, 7]
        print(self.ids)

    # 按excel每个用例依次传入并执行
    @allure.title("{title}")
    @pytest.mark.parametrize("num, title, is_run, model, level, description, domain, api, restype, headers, cookies, query, param, setup_data, teardown_data, extract, expected_data, response_data, black_list", self.case_list, ids=self.ids)
    def test_case(self, num, title, is_run, model, level, description, domain, api, restype, headers, cookies, query, param, setup_data, teardown_data, extract, expected_data, response_data, black_list):
        print('---------》', num, title)


if __name__ == '__main__':
    filepath = 'data/fast/suite/fast_auto_product_screen.xlsx'
    suite = TestSuite(filepath)
    pytest.main(['-s', '-x', "-o", "log_cli=true", "-o", "log_cli_level=INFO", r'ytest/utils/case/default_case.py'])

