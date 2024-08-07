#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :shell.py
@说明        :
@时间        :2023/05/11 16:04:36
@作者        :Leo
@版本        :1.0
"""

import subprocess


class Shell:
    @staticmethod
    def invoke(cmd):
        output, errors = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()
        o = output.decode("utf-8")
        return o
