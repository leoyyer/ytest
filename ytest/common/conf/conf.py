#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :conf.py
@说明        :
@时间        :2023/04/28 17:33:08
@作者        :Leo
@版本        :1.0
'''

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :conf.py
@说明        :
@时间        :2021/09/09 14:57:04
@作者        :Leo
@版本        :1.0
'''

from configparser import ConfigParser
import sys
import os
log_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(log_path)
from case.conftest import find_file,CASE_PATH



class Config:
    def __init__(self, project, conf=None):
        # 防止占位符给替换
        self.config = ConfigParser(interpolation=None)
        self.conf = f"{conf}.ini" if conf is not None else "conf.ini"
        self.conf_path = find_file(os.path.join(CASE_PATH, project), self.conf)
        self.config.read(self.conf_path, encoding='utf-8')


    def get_conf(self, title, value):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(title, value)

    def get_level(self):
        try:
            res = self.config.get("plan", 'level')
        except Exception:
            res = None
        return res


if __name__ == '__main__':
    Ctest = Config('fast')
    test = Ctest.get_conf('mysql', 'mysql_passwd')
    print(test)
