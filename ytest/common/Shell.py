#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :Shell.py
@说明        :
@时间        :2024/12/24 10:51:31
@作者        :Leo
@版本        :1.0
"""

import subprocess


class Shell:
    def __init__(self) -> None:
        pass

    @staticmethod
    def invoke(cmd):
        output, errors = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()
        o = output.decode("utf-8")
        return o

    def check_port_with_lsof(self, port):
        result = subprocess.run(
            f"lsof -i :{port}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.stdout:
            return True  # 端口已被占用
        return False  # 端口未被占用


shell = Shell()
