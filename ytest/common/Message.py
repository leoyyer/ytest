#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :wechat.py
@说明        :企业微信通知
@时间        :2024/10/24 16:43:27
@作者        :Leo
@版本        :1.0
"""
import requests, json


class Message:
    def __init__(self) -> None:
        pass

    def qywx(self, webhook_url, all_api, passed, failed, env):
        # 企业微信机器人的 Webhook URL
        webhook_url = webhook_url
        # 消息内容的 Markdown 格式
        message = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"**{env} 环境 - 冒烟用例执行完成**\n\n"
                f"总执行的用例数量: **{all_api}** \n"
                f"已通过的用例数量: **{passed}** \n"
                f"未通过的用例数量: **{failed}** \n"
                f"请映射端口查看详细报告。\n\n"
                f"> 注：请及时检查用例执行情况，避免遗漏重要问题。"
            },
        }
        # 将消息转换为 JSON 格式
        message_json = json.dumps(message)
        # 发送 POST 请求
        response = requests.post(webhook_url, data=message_json)
        if response.status_code == 200:
            print(f"消息发送成功: {response.text}")
        else:
            print(f"消息发送失败: {response.text}")


send_message = Message()
if __name__ == "__main__":
    send_message.qywx(
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d8a5b8e8-1f0e-49f2-8f3a-000a1a742fed",
        10,
        9,
        1,
        "test",
    )
