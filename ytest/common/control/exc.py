#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :exc.py
@说明        : 
@时间        :2023/04/24 17:42:53
@作者        :Leo
@版本        :1.0
'''

class CustomError(Exception):
    pass


class SQLAnalyzeError(CustomError):
    pass


class SQLExecuteError(CustomError):
    pass


class CaseExecuteError(CustomError):
    pass


class ParameterextractError(CustomError):
    pass


class SetupCaseError(CustomError):
    pass


class SetupError(CustomError):
    pass


class HookError(CustomError):
    pass


class ReadXlsError(CustomError):
    pass


class TemplateError(CustomError):
    pass


class CaseError(CustomError):
    pass


class FileError(CustomError):
    pass


class ExcelError(CustomError):
    pass


class CaseGenerateError(CustomError):
    pass


class AssertError(CustomError):
    pass


class FuncError(CustomError):
    pass


class RequestInterfaceError(CustomError):
    pass


class MongoExecuteError(CustomError):
    pass
