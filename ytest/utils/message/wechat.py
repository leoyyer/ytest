#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :wechat.py
@说明        :企业微信通知
@时间        :2024/10/24 16:43:27
@作者        :Leo
@版本        :1.0
"""

import requests
import json


def qywx(webhook_url, num, env):
    # 企业微信机器人的 Webhook URL
    webhook_url = webhook_url
    # 要发送的消息内容
    message = {
        "msgtype": "text",
        "text": {
            "content": f"{env}环境-冒烟用例执行完成,存在未通过的用例:{num},请映射端口查看详细报告。"
        },
    }
    # 将消息转换为 JSON 格式
    message_json = json.dumps(message)
    # 发送 POST 请求
    requests.post(webhook_url, data=message_json)


if __name__ == "__main__":
    qywx(
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d8a5b8e8-1f0e-49f2-8f3a-000a1a742fed",
        1,
        "test",
    )
