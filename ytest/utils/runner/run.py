#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :run.py
@说明        : 支持多进程运行(每个进程间的变量不互通)
@时间        :2023/05/11 18:24:32
@作者        :Leo
@版本        :1.0
'''
import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(base_path)
from case.conftest import get_file_path,CASE_PATH,find_file
from multiprocessing import Pool
import time
from ytest.common.control.shell import Shell
from functools import partial


def multi_process_run(project, floder=None, conf=None):
    """
    0. 判断项目和所需运行的文件夹,以及配置文件是否存在
    1. 遍历用例,过滤掉名字以_stop和._的开头的用例
    2. 组装参数,废弃原来的用例是否生成判断,默认生成
    """
    case_list = get_file_path(project, floder)
    print(case_list)
    if conf:
        _conf = f"{conf}.ini" if conf is not None else "conf.ini"
        # 验证conf.ini文件是否存在
        find_file(project, _conf)

    POOL_SIZE = 3  # 设置最大并发进程数
    with Pool(POOL_SIZE) as pool:
        print('conf',conf)
        # pool.map(run, case_list, conf)
        pool.map(partial(run, conf=conf),case_list)


def run(filename,conf):
    cmd = f'python ytest/utils/case/test_default_case.py --filename={filename} --conf={conf}'
    Shell.invoke(cmd)


if __name__ == '__main__':
    project = os.path.join(CASE_PATH, 'fast')
    multi_process_run(project, floder="suite", conf='test')
























