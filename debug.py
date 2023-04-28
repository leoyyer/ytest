# -*- coding: utf-8 -*-
import yaml
import argparse
template_file ='ytest/utils/templates/case.yaml'
def update_yaml_with_template(template_file: str, data_file: str) -> None:
    with open(template_file, 'r', newline='') as f:
        template = yaml.safe_load(f)

    with open(data_file, 'r', newline='') as f:
        data = yaml.safe_load(f)

    # 更新 base 部分数据
    base_data = {}
    for key, value in template['base'].items():
        if key in data['base']:
            if isinstance(value, type(data['base'][key])):
                base_data[key] = data['base'][key]
            else:
                base_data[key] = value
        else:
            base_data[key] = value

    # 更新 case 部分数据
    case_data = []
    for case in data['case']:
        new_case = {}
        for key, value in template['case'][0].items():
            if key in case:
                if isinstance(value, type(case[key])):
                    new_case[key] = case[key]
                else:
                    new_case[key] = value
            else:
                new_case[key] = value
        case_data.append(new_case)

    output = {'base': base_data, 'case': case_data}
    with open(data_file, 'w', newline='') as f:
        yaml.dump(output, f, default_flow_style=False)

# class DebugCaseList:
#     def __init__(self, case_file):
#         with open('ytest/utils/templates/case.yaml', 'r', encoding='utf-8') as f:
#             template = yaml.safe_load(f)
#         # 读取数据文件
#         with open(case_file, 'r', encoding='utf-8') as f:
#             data = yaml.safe_load(f)
#         # 更新模板数据
#        # 更新数据格式
#         for key, value in template.items():
#             if key not in data:
#                 data[key] = value
#             elif isinstance(value, dict):
#                 for sub_key, sub_value in value.items():
#                     if sub_key not in data[key]:
#                         data[key][sub_key] = sub_value
#             elif isinstance(value, list):
#                 for i in range(len(value)):
#                     if i >= len(data[key]):
#                         data[key].append(value[i])
#                     elif isinstance(value[i], dict):
#                         for sub_key, sub_value in value[i].items():
#                             if sub_key not in data[key][i]:
#                                 data[key][i][sub_key] = sub_value
#         # 将更新后的数据写入文件
#         with open(case_file, 'w', encoding='utf-8') as f:
#             yaml.dump(template, f, default_flow_style=False, allow_unicode=True)

        # with open(case_file, 'r', newline='') as f:
        #     self.test_suite = yaml.safe_load(f)
        # # 读取 base 部分数据
        # self.base_data = {}
        # print('---',self.test_suite.get('base'))
        # for item in self.test_suite.get('base', []):
        #     self.base_data.update(item)
        # self.base = {
        #     'base_url': self.base_data.get('base_url', ''),
        #     'blacklist': self.base_data.get('blacklist', []),
        #     'global_variable': self.base_data.get('global_variable', []),
        #     'global_assertion': self.base_data.get('global_assertion', []),
        #     'sql_assertion': self.base_data.get('sql_assertion', []),
        # }
    # def get_cases_by_num(self, case_num):
    #     """
    #     根据传入的 caseNum，返回一个包含需要调试的 case 的列表

    #     Args:
    #         caseNum (str): 需要调试的 case 的标识。当 caseNum 为 '- num: case_1' 时，返回 case_1 组的全部 case。
    #                        当 caseNum 为 'debug: ["case_1", "case_2"]' 时，返回 case_1 和 case_2 组的全部 case。
    #                        当 caseNum 为 'debug: ["case_1-case_3", "case_4"]' 时，返回 case_1 到 case_3 和 case_4 组的全部 case。

    #     Returns:
    #         list: 包含需要调试的 case 的列表

    #     """
    #     cases = []
    #     case_num = case_num.strip()
    #     if case_num.startswith('- num:'):
    #         # 如果 caseNum 是 '- num: case_1' 的格式
    #         num = case_num.split(':')[-1].strip()
    #         cases = [case for case in self.test_suite.get('case', []) if case.get('num') == num]
    #     elif case_num.startswith('debug:'):
    #         # 如果 caseNum 是 'debug: - case_1-case_2 - case_3' 或 'debug:  - case_1-case_2 - case_3' 的格式
    #         case_nums = self.test_suite.get('debug')
    #         print(case_nums)
    #         for case_num in case_nums:
    #             if '-' in case_num:
    #                 start, end = case_num.split('-')
    #                 start_num = int(start.split('_')[-1])
    #                 end_num = int(end.split('_')[-1])
    #                 cases.extend([case for case in self.test_suite.get('case', []) 
    #                               if start_num <= int(case.get('num').split('_')[-1]) <= end_num])
    #             else:
    #                 cases.extend([case for case in self.test_suite.get('case', []) if case.get('num') == case_num])
    #     else:
    #         raise ValueError(f'Invalid caseNum: {case_num}')

    #     if not cases:
    #         raise ValueError(f'Cannot find case: {case_num}')
    #     return {'base': self.base, 'case_list': cases}


def main():
    parser = argparse.ArgumentParser(description='Debug a test case by case number')
    parser.add_argument('case_file', type=str, help='path of the test case file')
    parser.add_argument('case_num', type=str, help='case number to debug')
    args = parser.parse_args()
    update_yaml_with_template(template_file,args.case_file)
    # case_list = debug_case_list.get_cases_by_num(args.case_num)
    # print(case_list)


if __name__ == '__main__':
    main()