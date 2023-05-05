#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_path)
import pytest
import allure
import argparse
from common.conf.conf import Config
from utils.case.case_run import get_case_detail
from common.control.read_xlsx import ReadXlsData
from utils.logger.logger import MyLog
parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, help="配置所需执行的用例路径")
parser.add_argument("--conf", help="配置指定的执行文件", default=None)
args = parser.parse_args()

log = MyLog(logger_name=__name__)

class TestSuite(object):
    excel = ReadXlsData(args.filename)
    case_detail = excel.get_case_data()
    conf_path = Config(case_detail['project'],args.conf)
    case_list = case_detail['case_list']
    env = conf_path.conf_path
    

    @allure.title("{title}")
    @pytest.mark.parametrize("case", case_list, ids=[case['case_id'] for case in case_list])
    def test_case(self, case):
        case_id, title, is_run, model, level, desc, domain, api, method, headers, cookies, param, body, setup, teardown, extract_data, expected_data, response, black_list = case.values()
        print('----2222-----》',case_id,title)
        print('----3333-----》',TestSuite.env)

    # @pytest.mark.parametrize("case_id, title, is_run, model, level, desc, domain, api, method, headers, cookies, param, body, setup, teardown, extract_data, expected_data, response", case_list, ids=ids)
    # def test_case(self, num, title, is_run, model, level, description, domain, api, restype, headers, cookies, query, param, setup_data, teardown_data, extract, expected_data, response_data, black_list):
    #     print('----2222-----》',num,title)

if __name__ == '__main__':
    # 运行测试用例
    pytest.main(['-s', '-v'])
