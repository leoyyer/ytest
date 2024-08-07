#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :project_initializer.py
@说明        :手脚架初始化
@时间        :2024/07/19 16:45:54
@作者        :Leo
@版本        :1.0
"""

import os
import shutil

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProjectInitializer:
    def __init__(self, project_name):
        self.project_name = project_name
        self.base_path = os.path.abspath(os.getcwd())
        self.case_dir = os.path.join(self.base_path, "case")
        self.project_dir = os.path.join(self.case_dir, project_name)
        self.api_dir = os.path.join(self.project_dir, "api")
        self.suite_dir = os.path.join(self.project_dir, "suite")
        self.ini_files = ["default.ini", "test.ini", "beta.ini", "prod.ini"]
        self.ini_content = """[project]
base_url = https://auto-test.mypaas.com
project_name = Auto Container Platform
project_team = Container group
tester = admin

[mysql]
mysql_host = xxxxx
mysql_port = 3306
mysql_user = root
mysql_passwd = xxxxx
"""
        self.hook_file = os.path.join(self.project_dir, "hook.py")
        self.hook_content = '''#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :hook.py
@说明        :用例执行时实时调用
                1.如果需要使用返回值必须return
                2.返回值如果是特定类型,必须指定类型
@作者        :Leo
@版本        :1.0
"""
import time
from datetime import datetime, timedelta
import json
import uuid


def generate_time_range(interval):
    "生成时间范围"
    data = {
        "from": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "to": (datetime.now() + timedelta(days=int(interval)))
        .replace(hour=23, minute=59, second=59)
        .strftime("%Y-%m-%d %H:%M:%S"),
    }
    return json.dumps(data)


def generate_id(user):
    # 获取当前时间戳（秒级）
    current_time = time.time()
    # 将秒级时间戳转换为毫秒级时间戳
    timestamp_13_digits = int(current_time * 1000)
    id = f"{user}-{str(timestamp_13_digits)}"
    return id


def generate_now_time():
    current_time = time.time()
    return str(current_time)


def generated_uuid(user):
    # 生成一个 UUID
    generated_uuid = uuid.uuid4()
    # 将 UUID 转换为字符串
    uuid_str = str(generated_uuid)
    user_code = f"{user}-{uuid_str}"
    return user_code

if __name__ == '__main__':
    generate_now_time()
'''
        self.demo_api_file = os.path.join(base_dir, "initializer", "demo_api.xlsx")
        self.demo_suite_file = os.path.join(base_dir, "initializer", "demo_suite.xlsx")

    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")
        else:
            print(f"Directory already exists: {path}")

    def create_file(self, path, content):
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(content)
            print(f"Created file: {path}")
        else:
            print(f"File already exists: {path}")

    def copy_demo_file(self):
        if os.path.exists(self.demo_api_file) or os.path.exists(self.demo_suite_file):
            api_dest_file = os.path.join(self.api_dir, "demo_api.xlsx")
            suite_dest_file = os.path.join(self.suite_dir, "demo_suite.xlsx")
            if not os.path.exists(api_dest_file):
                shutil.copy(self.demo_api_file, api_dest_file)
                print(f"Copied demo_api.xlsx to {api_dest_file}")
            else:
                print(f"demo_api.xlsx already exists in {api_dest_file}")
            if not os.path.exists(suite_dest_file):
                shutil.copy(self.demo_suite_file, suite_dest_file)
                print(f"Copied demo_suite.xlsx to {suite_dest_file}")
            else:
                print(f"demo_suite.xlsx already exists in {suite_dest_file}")

        else:
            print(f"demo_api.xlsx or demo_suite.xlsx not found in {self.base_path}")

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


if __name__ == "__main__":
    project_initializer = ProjectInitializer("demo")
    project_initializer.initialize_project()
