#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :project_initializer.py
@说明        :手脚架初始化
@时间        :2024/07/19 16:45:54
@作者        :Leo
@版本        :1.0
'''

import os
import shutil
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProjectInitializer:
    def __init__(self, project_name):
        self.project_name = project_name
        self.base_path = os.path.abspath(os.getcwd())
        self.case_dir = os.path.join(self.base_path, 'case')
        self.project_dir = os.path.join(self.case_dir, project_name)
        self.api_dir = os.path.join(self.project_dir, 'api')
        self.suite_dir = os.path.join(self.project_dir, 'suite')
        self.ini_files = ['default.ini', 'test.ini', 'beta.ini', 'prod.ini']
        self.ini_content = '''[project]
base_url = https://auto-test.mypaas.com
project_name = Auto Container Platform
project_team = Container group
tester = admin

[mysql]
mysql_host = xxxxx
mysql_port = 3306
mysql_user = root
mysql_passwd = xxxxx
'''
        self.hook_file = os.path.join(self.project_dir, 'hook.py')
        self.hook_content = '''def test_demo(demo):
    return demo


if __name__ == '__main__':
    test_demo(demo)
'''
        self.demo_file = os.path.join(base_dir, 'initializer', 'demo.xlsx')

    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")
        else:
            print(f"Directory already exists: {path}")

    def create_file(self, path, content):
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(content)
            print(f"Created file: {path}")
        else:
            print(f"File already exists: {path}")

    def copy_demo_file(self):
        print(self.demo_file)
        if os.path.exists(self.demo_file):
            for folder in [self.api_dir, self.suite_dir]:
                dest_file = os.path.join(folder, 'demo.xlsx')
                if not os.path.exists(dest_file):
                    shutil.copy(self.demo_file, dest_file)
                    print(f"Copied demo.xlsx to {folder}")
                else:
                    print(f"demo.xlsx already exists in {folder}")
        else:
            print(f"demo.xlsx not found in {self.base_path}")

    def initialize_project(self):
        # 创建文件夹
        self.create_dir(self.case_dir)
        self.create_dir(self.project_dir)
        self.create_dir(self.api_dir)
        self.create_dir(self.suite_dir)
        
        # 创建 ini 文件
        for ini_file in self.ini_files:
            file_path = os.path.join(self.project_dir, ini_file)
            self.create_file(file_path, self.ini_content)
        
        # 创建 hook.py 文件
        self.create_file(self.hook_file, self.hook_content)

        # 拷贝 demo.xlsx 文件
        self.copy_demo_file()


if __name__ == '__main__':
    project_initializer = ProjectInitializer('log_servers')
    project_initializer.initialize_project()
