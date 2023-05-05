import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_path)
import pytest
from utils.logger.logger import MyLog
from common.control.read_xlsx import ReadXlsData
from common.conf.conf import Config
import allure
import unittest
from utils.case.case_run import CASE_DETAIL,get_case_detail

import sys
import os
import unittest
from utils.logger.logger import MyLog
from common.control.read_xlsx import ReadXlsData
from common.conf.conf import Config
import allure
from utils.case.case_run import CASE_DETAIL,get_case_detail

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, help="Excel file path")
args = parser.parse_args()


class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.filename = args.filename
        self.excel = ReadXlsData(self.filename)
        self.case_detail = self.excel.get_case_data()
        self.conf = Config(self.case_detail['project'])
        self.env = self.conf.conf_path
    
    def case(self,num, case_id, title, is_run, model, level, desc, domain, api, method, headers, cookies, param, body, setup,teardown, extract_data, expected_data, response, black_list):
        print('---------》',num,title)

    def case_parametrize(self):
        print(2222)
        for i, case in enumerate(self.case_detail["case_list"]):
            num = i
            case_id = case['case_id']
            title = case['title']
            is_run = case['is_run']
            model = case['model']
            level = case['level']
            desc= case['desc']
            domain = case['domain']
            api = case['api']
            method = case['method']
            headers = case['headers']
            cookies = case['cookies']
            param = case['param']
            body = case['body']
            setup = case['setup']
            teardown = case['teardown']
            extract_data = case['extract_data']
            expected_data = case['expected_data']
            response = case['response']
            black_list = case['black_list']
            yield (num, case_id, title, is_run, model, level, desc, domain, api, method, headers, cookies, param, body, setup,teardown, extract_data, expected_data, response, black_list)

    def test_run_cases(self):
        print(1111)
        self.setUp()
        for args in self.case_parametrize():
            self.case(*args)


if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, help="Excel file path")
    args = parser.parse_args()
    
    # 将命令行参数传递给测试类
    TestSuite.filename = args.filename
    
    # 运行测试用例
    unittest.main()


# if __name__ == '__main__':
#     unittest.main()

# class TestSuite(unittest.TestCase):
    
#     def __init__(self, filename: str, conf = None):
#         self.filename = filename
#         self.excel = ReadXlsData(self.filename)
#         self.case_detail = self.excel.get_case_data()
#         self.conf = Config(self.case_detail['project'],conf)
#         self.env = self.conf.conf_path

#     @allure.title("{title}")
#     def case(self,num, case_id, title, is_run, model, level, desc, domain, api, method, headers, cookies, param, body, setup,teardown, extract_data, expected_data, response, black_list):
#         print('---------》',num,title)

#     def case_parametrize(self):
#         print(2222)
#         for i, case in enumerate(self.case_detail["case_list"]):
#             num = i
#             case_id = case['case_id']
#             title = case['title']
#             is_run = case['is_run']
#             model = case['model']
#             level = case['level']
#             desc= case['desc']
#             domain = case['domain']
#             api = case['api']
#             method = case['method']
#             headers = case['headers']
#             cookies = case['cookies']
#             param = case['param']
#             body = case['body']
#             setup = case['setup']
#             teardown = case['teardown']
#             extract_data = case['extract_data']
#             expected_data = case['expected_data']
#             response = case['response']
#             black_list = case['black_list']
#             yield (num, case_id, title, is_run, model, level, desc, domain, api, method, headers, cookies, param, body, setup,teardown, extract_data, expected_data, response, black_list)

#     def test_run_cases(self):
#         print(1111)
#         for args in self.case_parametrize():
#             self.case(*args)


# if __name__ == '__main__':
#     ts = TestSuite('data/fast/suite/fast_auto_product_screen.xlsx')
#     pytest.main([ "-v", 'ytest/utils/case/test_case_default.py', '-k', 'test_run_cases'])
