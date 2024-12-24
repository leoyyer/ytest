#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :CaseBlowUp.py
@说明        : 通过各种方式生成api的用例
@时间        :2024/08/07 11:43:32
@作者        :Leo
@版本        :1.0
"""
import json, os
from itertools import product
import pandas as pd


class CaseBlowUp:
    def __init__(self, projectName, excelName, valueType):
        self.project_name = projectName
        self.base_path = os.path.abspath(os.getcwd())
        self.case_dir = os.path.join(self.base_path, "case")
        self.project_dir = os.path.join(self.case_dir, projectName)
        self.api_dir = os.path.join(self.project_dir, "api")
        self.excel_path = os.path.join(self.api_dir, excelName)
        self.valueType = valueType
        self.original_json = {}
        self.equivalence_classes = {}
        self.boundary_values = {}
        self.decision_table = []
        self.error_guessing = {}

    def parse_excel_and_generate_tests(self):
        # 读取 Excel 文件
        df_inflation = pd.read_excel(self.excel_path, sheet_name="value_inflation")
        df_case = pd.read_excel(self.excel_path, sheet_name="case")
        # 过滤掉列名包含 'Unnamed' 的列
        df_case = df_case.loc[:, ~df_case.columns.str.contains("^Unnamed")]

        # 处理 value_inflation 标签
        for index, row in df_inflation.iterrows():
            key = row.iloc[0]
            value = row.iloc[1]
            # 检查 value 是否为空（NaN）
            if pd.isna(value):
                continue
            try:
                # 确保 JSON 字符串使用双引号
                value = value.replace("'", '"')
                parsed_value = json.loads(value)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for key {key}: {e}")
                continue

            if "等价类" in key:
                self.equivalence_classes.update(parsed_value)
            elif "边界值" in key:
                self.boundary_values.update(parsed_value)
            elif "判定表" in key:
                self.decision_table.extend(parsed_value)
            elif "错误推断" in key:
                self.error_guessing.update(parsed_value)

        # 检查 df_case 的行数
        if df_case.shape[0] < 1:
            print("Error: The 'case' sheet does not contain enough rows.")
            return

        # 获取表头
        headers = df_case.columns.tolist()
        # 处理 case 标签
        case_values = df_case.iloc[0].tolist()
        case_dict = dict(zip(headers, case_values))
        if self.valueType == "body":
            if "body参数" in case_dict:
                try:
                    self.original_json = json.loads(
                        case_dict["body参数"].replace("'", '"')
                    )
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for original_json: {e}")
        elif self.valueType == "param":
            if "param参数" in case_dict:
                if isinstance(case_dict["param参数"], str):
                    try:
                        self.original_json = json.loads(
                            case_dict["body参数"].replace("'", '"')
                        )
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON for original_json: {e}")

        if (
            self.equivalence_classes == {}
            and self.boundary_values == {}
            and self.decision_table == []
            and self.error_guessing == {}
            and self.original_json == {}
        ):
            pass
        elif self.original_json == {}:
            pass
        else:
            # 生成测试用例
            test_cases = self.generate_test_cases()
            # 将生成的测试用例写入 Excel 文件
            new_rows = []
            # 使用 enumerate 遍历
            for index, test_case in enumerate(test_cases):
                new_row = case_dict.copy()
                new_row["序号"] = f"case_{str(index + 2)}"
                new_row["描述"] = test_case["description"]
                if self.valueType == "body":
                    new_row["body参数"] = json.dumps(test_case["test_case"])
                elif self.valueType == "param":
                    new_row["param参数"] = json.dumps(test_case["test_case"])
                new_rows.append(new_row)

            new_df = pd.DataFrame(new_rows)
            with pd.ExcelWriter(
                self.excel_path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                new_df.to_excel(
                    writer,
                    sheet_name="case",
                    startrow=len(df_case) + 1,
                    index=False,
                    header=False,
                )

    # 正交法（选择性组合）
    def orthogonal_combinations(self):
        keys = self.equivalence_classes.keys()
        values = [self.equivalence_classes[key] for key in keys]
        return [dict(zip(keys, comb)) for comb in product(*values)]

    # 笛卡尔系数（所有组合）
    def cartesian_product(self):
        keys = self.equivalence_classes.keys()
        values = [self.equivalence_classes[key] for key in keys]
        return [dict(zip(keys, comb)) for comb in product(*values)]

    def generate_test_cases(self):
        test_cases = set()
        # 等价类
        for key, values in self.equivalence_classes.items():
            for value in values:
                test_case = self.original_json.copy()
                test_case[key] = value
                description = f"Equivalence class test for {key} with value {value}."
                test_cases.add(
                    json.dumps({"test_case": test_case, "description": description})
                )

        # 边界值
        for key, values in self.boundary_values.items():
            for value in values:
                test_case = self.original_json.copy()
                test_case[key] = value
                description = f"Boundary value test for {key} with value {value}."
                test_cases.add(
                    json.dumps({"test_case": test_case, "description": description})
                )

        # 判定表
        for case in self.decision_table:
            description = "Decision table test case."
            test_cases.add(json.dumps({"test_case": case, "description": description}))

        # 错误推断
        for key, values in self.error_guessing.items():
            for value in values:
                test_case = self.original_json.copy()
                test_case[key] = value
                description = f"Error guessing test for {key} with value {value}."
                test_cases.add(
                    json.dumps({"test_case": test_case, "description": description})
                )

        # 正交法
        orthogonal_cases = self.orthogonal_combinations()
        for case in orthogonal_cases:
            description = "Orthogonal array test case."
            test_cases.add(json.dumps({"test_case": case, "description": description}))

        # 笛卡尔系数
        cartesian_cases = self.cartesian_product()
        for case in cartesian_cases:
            description = "Cartesian product test case."
            test_cases.add(json.dumps({"test_case": case, "description": description}))

        return [json.loads(test_case) for test_case in test_cases]


if __name__ == "__main__":
    # 替换为你的Excel文件路径
    test_data = CaseBlowUp("fast", "demo_api.xlsx", "body")
    test_data.parse_excel_and_generate_tests()
