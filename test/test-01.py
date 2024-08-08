import json
from itertools import product
import pandas as pd


def parse_excel_and_generate_tests(excel_path, valueType):
    # 读取 Excel 文件
    df_inflation = pd.read_excel(excel_path, sheet_name="value_inflation")
    df_case = pd.read_excel(excel_path, sheet_name="case")
    # 过滤掉列名包含 'Unnamed' 的列
    df_case = df_case.loc[:, ~df_case.columns.str.contains("^Unnamed")]

    # 初始化全局变量
    global original_json, equivalence_classes, boundary_values, decision_table, error_guessing
    original_json = {}
    equivalence_classes = {}
    boundary_values = {}
    decision_table = []
    error_guessing = {}

    # 处理 value_inflation 标签
    for index, row in df_inflation.iterrows():
        key = row.iloc[0]
        value = row.iloc[1]
        try:
            # 确保 JSON 字符串使用双引号
            value = value.replace("'", '"')
            parsed_value = json.loads(value)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for key {key}: {e}")
            continue

        if "等价类" in key:
            equivalence_classes.update(parsed_value)
        elif "边界值" in key:
            boundary_values.update(parsed_value)
        elif "判定表" in key:
            decision_table.extend(parsed_value)
        elif "错误推断" in key:
            error_guessing.update(parsed_value)

    # 检查 df_case 的行数
    if df_case.shape[0] < 1:
        print("Error: The 'case' sheet does not contain enough rows.")
        return

    # 获取表头
    headers = df_case.columns.tolist()
    # 处理 case 标签
    case_values = df_case.iloc[0].tolist()
    case_dict = dict(zip(headers, case_values))
    if valueType == "body":
        if "body参数" in case_dict:
            try:
                original_json = json.loads(case_dict["body参数"].replace("'", '"'))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for original_json: {e}")
    elif valueType == "param":
        if "param参数" in case_dict:
            if isinstance(case_dict["param参数"], str):
                try:
                    original_json = json.loads(case_dict["body参数"].replace("'", '"'))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for original_json: {e}")

    if (
        equivalence_classes == {}
        and boundary_values == {}
        and decision_table == []
        and error_guessing == {}
    ):
        pass
    else:
        # 生成测试用例
        test_cases = generate_test_cases()
        # 将生成的测试用例写入 Excel 文件
        new_rows = []
        # 使用 enumerate 遍历
        for index, test_case in enumerate(test_cases):
            new_row = case_dict.copy()
            new_row["序号"] = f"case_{str(index + 2)}"
            new_row["描述"] = test_case["description"]
            if valueType == "body":
                new_row["body参数"] = json.dumps(test_case["test_case"])
            elif valueType == "param":
                new_row["param参数"] = json.dumps(test_case["test_case"])
            new_rows.append(new_row)

        new_df = pd.DataFrame(new_rows)
        with pd.ExcelWriter(
            excel_path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
        ) as writer:
            new_df.to_excel(
                writer,
                sheet_name="case",
                startrow=len(df_case) + 1,
                index=False,
                header=False,
            )


# 正交法（选择性组合）
def orthogonal_combinations(equivalence_classes):
    keys = equivalence_classes.keys()
    values = [equivalence_classes[key] for key in keys]
    return [dict(zip(keys, comb)) for comb in product(*values)]


# 笛卡尔系数（所有组合）
def cartesian_product(values_dict):
    keys = values_dict.keys()
    values = [values_dict[key] for key in keys]
    return [dict(zip(keys, comb)) for comb in product(*values)]


def generate_test_cases():
    test_cases = set()
    # 等价类
    for key, values in equivalence_classes.items():
        for value in values:
            test_case = original_json.copy()
            test_case[key] = value
            description = f"Equivalence class test for {key} with value {value}."
            test_cases.add(
                json.dumps({"test_case": test_case, "description": description})
            )

    # 边界值
    for key, values in boundary_values.items():
        for value in values:
            test_case = original_json.copy()
            test_case[key] = value
            description = f"Boundary value test for {key} with value {value}."
            test_cases.add(
                json.dumps({"test_case": test_case, "description": description})
            )

    # 判定表
    for case in decision_table:
        description = "Decision table test case."
        test_cases.add(json.dumps({"test_case": case, "description": description}))

    # 错误推断
    for key, values in error_guessing.items():
        for value in values:
            test_case = original_json.copy()
            test_case[key] = value
            description = f"Error guessing test for {key} with value {value}."
            test_cases.add(
                json.dumps({"test_case": test_case, "description": description})
            )

    # 正交法
    orthogonal_cases = orthogonal_combinations(equivalence_classes)
    for case in orthogonal_cases:
        description = "Orthogonal array test case."
        test_cases.add(json.dumps({"test_case": case, "description": description}))

    # 笛卡尔系数
    cartesian_cases = cartesian_product(equivalence_classes)
    for case in cartesian_cases:
        description = "Cartesian product test case."
        test_cases.add(json.dumps({"test_case": case, "description": description}))

    return [json.loads(test_case) for test_case in test_cases]


if __name__ == "__main__":
    excel_path = "/Users/leo/workspace/ytest/case/fast/api/demo-1.xlsx"  # 替换为你的Excel文件路径
    parse_excel_and_generate_tests(excel_path, "body")
