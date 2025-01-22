#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :Allure.py
@说明        :
@时间        :2024/12/23 17:01:57
@作者        :Leo
@版本        :1.0
"""

import json, os, allure
from jinja2 import Environment, FileSystemLoader
from ytest.config.ConfFile import ConfigFile
from ytest.conf import config


CATEGORIES = [
    {"name": "Ignored tests", "matchedStatuses": ["skipped"]},
    {
        "name": "Infrastructure problems",
        "matchedStatuses": ["broken", "failed"],
        "messageRegex": ".*bye-bye.*",
    },
    {
        "name": "断言异常",
        "matchedStatuses": ["failed"],
        "messageRegex": ".*AssertionError.*",
    },
    {
        "name": "Outdated tests",
        "matchedStatuses": ["broken"],
        "traceRegex": ".*FileNotFoundException.*",
    },
    {"name": "接口异常缺陷", "matchedStatuses": ["failed"]},
    {"name": "测试异常缺陷", "matchedStatuses": ["broken"]},
]


class Allure:
    def __init__(self) -> None:
        pass

    def allure_data(self, params):
        """[summary]
        在allure中,规范输出需要展示的内容
        Args:
        params ([type]): [description]
        """
        target = ""
        try:
            if isinstance(params, dict):
                if "text" in params:
                    params.pop("text")
                target = json.dumps(
                    params,
                    sort_keys=True,
                    indent=4,
                    separators=(",", ":"),
                    ensure_ascii=False,
                )
            else:
                data = json.loads(params)
                target = json.dumps(
                    data,
                    sort_keys=True,
                    indent=4,
                    separators=(",", ":"),
                    ensure_ascii=False,
                )
        except Exception:
            target = params
        return target

    def allure_step(self, step: str, var: str) -> None:
        """
        :param step: 步骤及附件名称
        :param var: 附件内容
        """
        var = json.loads(var)
        with allure.step(step):
            allure.attach(
                json.dumps(var, ensure_ascii=False, indent=4),
                step,
                allure.attachment_type.JSON,
            )

    def allure_step_no(self, step: str):
        """
        无附件的操作步骤
        :param step: 步骤名称
        :return:
        """
        with allure.step(step):
            pass

    def allure_title(self, title: str) -> None:
        """allure中显示的用例标题"""
        allure.dynamic.title(title)

    def add_environment(self, project, path):
        """[summary]
        allure报告首页overview-环境变量设置处不支持中文
        Args:
            path ([type]): [description]
        """
        conf = ConfigFile(project=project)
        template_path = os.path.join(config.ytest_path, "ytest", "templates")
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template("environment")
        base_url = conf.get_conf("project", "base_url")
        project_name = conf.get_conf("project", "project_name")
        project_team = conf.get_conf("project", "project_team")
        tester = conf.get_conf("project", "tester")
        # 生成对应的用例名
        filename = "environment.properties"
        # 模版内容生成
        content = template.render(
            base_url=base_url,
            project_name=project_name,
            project_team=project_team,
            tester=tester,
        )
        with open(path + "/" + filename, "w", encoding="utf-8") as fp:
            fp.write(content)
            fp.close()

    def add_categories(self, path):
        """_summary_
        allure报告首页-CATEGORIES(测试用例结果的分类)增加配置
        Args
            path (_type_): _description_
        """
        filename = "categories.json"
        with open(os.path.join(path, filename), "w", encoding="utf-8") as fp:
            json.dump(CATEGORIES, fp, ensure_ascii=False, indent=4)

    def get_previous_timestamp_folders(self, base_path, current_timestamp):
        """
        获取基于当前时间戳之前的最多5个时间戳文件夹名（按日期倒序排序，日期相同则按_id排序）
        Args:
            base_path (str): 基础路径
            current_timestamp (str): 当前时间戳（格式：YYYYMMDD_reportId）
        Returns:
            list: 时间戳文件夹名列表
        """
        timestamp_folders = []
        # 提取当前时间戳中的日期和报告 ID
        current_date = current_timestamp.split("_")[0]
        current_report_id = current_timestamp.split("_")[1]
        # 获取 base_path 下所有文件夹
        all_folders = os.listdir(base_path)
        # 遍历文件夹
        for folder_name in all_folders:
            folder_path = os.path.join(base_path, folder_name)
            # 确保是目录，并且文件夹名符合 {YYYYMMDD_report_id} 的格式
            if os.path.isdir(folder_path) and "_" in folder_name:
                date_part, report_id = folder_name.split("_")
                # 如果日期部分是数字，表示有效的日期
                if date_part.isdigit() and len(date_part) == 8:
                    # 如果文件夹与当前时间戳相同，跳过
                    if date_part == current_date and report_id == current_report_id:
                        continue

                    # 如果文件夹的日期小于当前时间戳，则加入列表
                    timestamp_folders.append((folder_name, date_part, report_id))
        # 按照日期倒序排序，如果日期相同则按照 report_id 排序
        timestamp_folders.sort(key=lambda x: (x[1], x[2]), reverse=True)
        # 只返回最多7个文件夹的名称
        timestamp_folders = [folder[0] for folder in timestamp_folders[:7]]
        return timestamp_folders

    def merge_history_trend(self, base_path, current_timestamp, timestamp_folders):
        """
        获取最新报告的执行情况，把历史的history-trend.json(默认上一个,可配置)数据追加上去
        Args:
            base_path (str): 基础路径
            current_timestamp (str): 当前时间戳
            timestamp_folders (list): 时间戳文件夹名列表
        Returns:
            dict: 合并后的 history-trend.json 数据
        """
        now_trend_path = os.path.join(base_path, current_timestamp, "allure-report", "history", "history-trend.json")
        with open(now_trend_path, "r", encoding="utf-8") as file:
            now_trend_data = json.load(file)
            now_trend_data[0]["buildOrder"] = current_timestamp
        current_history_trend = {"items": now_trend_data}  # 初始化为最新报告中的执行情况
        current_history_trend = {"items": []}
        # 遍历时间戳文件夹列表
        for timestamp_folder in timestamp_folders:
            history_trend_path = os.path.join(base_path, timestamp_folder, "allure-report", "history", "history-trend.json")
            # 判断文件是否存在
            if not os.path.exists(history_trend_path):
                continue
            # 读取 history-trend.json 文件数据
            with open(history_trend_path, "r", encoding="utf-8") as file:
                history_trend_data = json.load(file)
                if current_history_trend is None:
                    current_history_trend = history_trend_data
                else:
                    # 确保 history-trend.json 数据是字典类型
                    if isinstance(history_trend_data, list):
                        # 逐个添加列表中的字典元素
                        for item in history_trend_data:
                            if isinstance(item, dict):
                                item["buildOrder"] = timestamp_folder
                                current_history_trend["items"].append(item)
                            else:
                                print(f"Warning: history-trend.json in {timestamp_folder} contains invalid data.")
                    else:
                        print(f"Warning: history-trend.json in {timestamp_folder} is not a list.")
        new_history_trend = self.sort_and_filter_build_orders(current_history_trend, count=7)
        return new_history_trend

    def write_history_trend(self, data, base_path, timestamp_folder):
        """_summary_
        把之前的执行历史重新写入最新生成报告中的history-trend.json文件中
        Args:
            data (_type_): 最大10分历史数据的执行情况
            base_path (_type_): 报告路径
            timestamp_folder (_type_): 最新的报告时间戳
        """
        file_path = os.path.join(base_path, timestamp_folder, "allure-report", "widgets", "history-trend.json")
        # 将新的字典转换成 JSON 格式
        json_data = json.dumps(
            data["items"],
            indent=4,
            ensure_ascii=False,
        )
        # 写入到 history-trend.json 文件中
        with open(file_path, "w") as file:
            file.write(json_data)

    def add_history_trend(self, base_path, current_timestamp):
        # 创建必要的目录
        timestamp_folders = self.get_previous_timestamp_folders(base_path, current_timestamp)
        merged_history_trend = self.merge_history_trend(base_path, current_timestamp, timestamp_folders)
        self.write_history_trend(merged_history_trend, base_path, current_timestamp)

    def sort_and_filter_build_orders(self, data, count=7):
        """
        对历史数据进行排序和去重, 倒叙获取最后指定数量的元素。

        :param data: 包含多个构建记录的字典，格式为 {'items': [...]}
        :param count: 需要返回的最大元素数量，默认为7
        :return: 排序后最新的 `count` 条数据
        """
        # 确保输入数据为字典，并且包含 'items' 键
        if not isinstance(data, dict) or "items" not in data or not isinstance(data["items"], list):
            raise ValueError("输入数据必须是包含 'items' 键的字典，且 'items' 必须是列表")

        # 提取 'items' 列表
        items = data["items"]

        # 去重，以 buildOrder 作为唯一键，保留最新的
        unique_data = {entry["buildOrder"]: entry for entry in items}

        # 按 buildOrder 进行倒序排序 (日期_编号)
        sorted_data = sorted(unique_data.values(), key=lambda x: tuple(map(int, x["buildOrder"].split("_"))), reverse=True)

        # 获取最后 `count` 个结果
        return {"items": sorted_data[:count]}


yallure = Allure()
