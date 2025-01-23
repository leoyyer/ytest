#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :hook_temp.py
@说明        :
@时间        :2022/08/24 16:05:06
@作者        :Leo
@版本        :1.0
"""

hook_content = '''#!/usr/bin/env python
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
    generate_now_time()'''
