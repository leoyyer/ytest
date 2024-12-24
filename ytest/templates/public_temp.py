#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :public_temp.py
@说明        :
@时间        :2024/12/24 16:06:03
@作者        :Leo
@版本        :1.0
"""

public_content = """
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :public.py
@说明        :cace层级的通用hook函数
@时间        :2022/08/30 17:33:26
@作者        :Leo
@版本        :1.0
'''
from datetime import datetime, timedelta
from icecream import ic

def generated_detetime(days=None,date_type="st"):
    if days:
        # 获取明天的时间
        _time = datetime.now() + timedelta(days=int(days))
    else:
        _time = datetime.now()
     # 转换成指定的格式
    if date_type == 'st':
        specific_formatted_time = _time.strftime('%Y-%m-%d 00:00:00')
    else:
        specific_formatted_time = _time.strftime('%Y-%m-%d 23:59:59')
    return specific_formatted_time


if __name__ == '__main__':
    ic(generated_detetime())
        """
