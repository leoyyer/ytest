#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :File.py
@说明        :对目录进行统一处理
@时间        :2024/12/20 17:20:32
@作者        :Leo
@版本        :1.0
"""
import os, sys, shutil


class Flile:
    def __init__(self):
        pass

    def find_file(self, _folder: str, file_name) -> str:
        """_summary_

        Args:
            _folder (str): 文件的绝对路径
            file_name (str): 需要判断的文件名

        Raises:
            FileNotFoundError: 文件不存在

        Returns:
            str: 返回存在文件的绝对路径
        """
        current_floder = os.path.abspath(_folder)
        parent_floder = os.path.dirname(current_floder)
        for root, dirs, files in os.walk(current_floder):
            if file_name in files:
                return os.path.join(root, file_name)
        for root, dirs, files in os.walk(parent_floder):
            if file_name in files:
                return os.path.join(root, file_name)

        raise FileNotFoundError(f"路径:{parent_floder},项目不存在{file_name},请检查！")

    def find_folder(self, folder_name: str, _path=None):
        if _path is None:
            # 返回当前工作目录的绝对路径
            _path = os.path.abspath(".")
        for root, dirs, files in os.walk(_path):
            if folder_name in dirs:
                folder_path = os.path.join(root, folder_name)
                # 把目录添加到内存中
                sys.path.append(folder_path)
                return folder_path
        raise FileNotFoundError(f"项目不存在{folder_name},请检查！")

    def get_file_path(self, folder, file=None):
        # 返回指定的文件夹包含的文件或文件夹的名字的列表
        ini_files = [
            f
            for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f)) and f.endswith(".ini")
        ]
        if not ini_files:
            raise FileNotFoundError(f"{folder} 下,ini 配置文件不存在,请检查")
        if file is None:
            # 遍历folder下的全部文件夹，筛选出.xlsx文件
            case_list = []
            for root, dirs, files in os.walk(folder):
                for name in files:
                    if (
                        name.endswith(".xlsx")
                        and "_stop" not in name
                        and "._" not in name
                    ):
                        case_list.append(os.path.join(root, name))
        else:
            # 判断路径是否存在
            path = os.path.join(folder, file)
            if not os.path.exists(path):
                raise Exception(f"{folder} 下, 文件 {file} 不存在,请检查")
            # 遍历路径下的全部文件夹，筛选出.xlsx文件
            case_list = []
            for root, dirs, files in os.walk(path):
                for name in files:
                    if (
                        name.endswith(".xlsx")
                        and "_stop" not in name
                        and "._" not in name
                    ):
                        case_list.append(os.path.join(root, name))
        if len(case_list):
            return case_list
        else:
            raise Exception(f"{folder} 下不存在测试用例,请检查")

    def default_folder(self, directory_path: str):
        # 尝试删除目录
        try:
            shutil.rmtree(directory_path)
        except FileNotFoundError:
            # 如果目录不存在，则创建它
            os.makedirs(directory_path)


file_operate = Flile()
