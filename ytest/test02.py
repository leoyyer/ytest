import json

data = {
	'file_name': 'fast_app_product_screen.xlsx',
	'case_name': 'fast_app_product_screen',
	'type': 'suite',
	'project': 'fast',
	'base': {
		'project_name': 'Fast Container Platform',
		'project_team': 'Container group',
		'base_url': 'https://fast-test.mypaas.com',
		'environment': 'auto-test',
		'tester': 'admin',
		'desc': 'auto_app_product 产品实时大屏',
		'blacklist': ['a', 'b', 'c', 'd'],
		'global_variable': {
			'username': 'pengda01',
			'password': '123456.0',
			'url': 'https://mks-test.mypaas.com/auth-api/v2/user/login',
			'now': None,
			'token': 'cc30e4e710c85b3f033d34d26bc06bbc02399bc9',
			'new_bee': None,
			'mks_env_tag': 'prod',
			'num': '3600.0',
			'feature_name': '我是测试数据'
		},
		'base_assert': [{
			'type': 'response_code',
			'text': '200'
		}, {
			'type': 'response_code',
			'text': '400'
		}],
		'sql_list': [{
			'1': {
				'type': 'mysql',
				'database': 'api_test_starship_rbac',
				'sql': "select id as groups_id from rbac_group where name = 'CI组合场景自动化'",
				'key': 'groups_id'
			}
		}, {
			'2': {
				'type': 'mysql',
				'database': 'api_test_starship_rbac',
				'sql': "select id as groups_id from rbac_group where name = 'CI组合场景自动化'"
			}
		}, {
			'3': {
				'type': 'mysql',
				'database': 'api_test_starship_rbac',
				'sql': "select id as groups_id from rbac_group where name = '我是测试数据'"
			}
		}],
		'case_len': 8
	},
	'case_list': [{
		'case_id': 'case_01',
		'title': '用户登录',
		'is_run': '是',
		'model': 'authapi',
		'level': 'P1',
		'desc': '自动化测试账号登录',
		'domain': 'https://fast-test.mypaas.com',
		'api': '/authapi/user/login/pengda01/123',
		'headers': {
			'envcode': 'prod',
			'x-fast-tenant': 'auto',
			'tenantcode': 'auto',
			'authorization': 'cc30e4e710c85b3f033d34d26bc06bbc02399bc9',
			'x-fast-user': 'pengda01',
			'x-fast-trace-id': 'fast-25575f287a0f620-0f820015a2-b3303153'
		},
		'cookies': '',
		'param': '',
		'body': {
			'account': 'pengda01',
			'password': '123456.0',
			'auto_login': 0
		},
		'setup': {
			'type': 'mysql',
			'database': 'api_test_starship_branch',
			'sql': "select id as feature_id from feature where name = '我是测试数据'",
			'key': 'feature_id'
		},
		'treandown': {
			'type': 'mysql',
			'database': 'api_test_starship_rbac',
			'sql': "select id as groups_id from rbac_group where name = 'CI组合场景自动化'",
			'key': 'groups_id'
		},
		'extract_data': [{
			'type': 'response_code',
			'text': '200'
		}, {
			'type': 'response_code',
			'text': '400'
		}],
		'response': '',
		'black_list': ['1', '2', '3', '4', '5']
	}, {
		'case_id': 'case_02',
		'title': '用户登录',
		'is_run': '是',
		'model': 'authapi',
		'level': 'P1',
		'desc': '自动化测试账号登录',
		'domain': 'https://fast-test.mypaas.com',
		'api': '/authapi/user/login/pengda01/123',
		'headers': {
			'envcode': 'prod',
			'x-fast-tenant': 'auto',
			'tenantcode': 'auto',
			'authorization': 'cc30e4e710c85b3f033d34d26bc06bbc02399bc9',
			'x-fast-user': 'pengda01',
			'x-fast-trace-id': 'fast-25575f287a0f620-0f820015a2-b3303153'
		},
		'cookies': '',
		'param': '',
		'body': {
			'account': '${user_name}',
			'password': '${pwd}',
			'auto_login': 0
		},
		'setup': {
			'type': 'mysql',
			'database': 'api_test_starship_branch',
			'sql': "select id as feature_id from feature where name = '我是测试数据'",
			'key': 'feature_id'
		},
		'treandown': {
			'type': 'mysql',
			'database': 'api_test_starship_rbac',
			'sql': "select id as groups_id from rbac_group where name = 'CI组合场景自动化'",
			'key': 'groups_id'
		},
		'extract_data': [{
			'type': 'response_code',
			'text': '400'
		}, {
			'type': 'response_code',
			'text': '200'
		}, {
			'type': 'response_body',
			'text': 'code=2000;msg=成功'
		}],
		'response': '',
		'black_list': ['3.0']
	}, {
		'case_id': 'case_03',
		'title': 'healthmetricscore_serverandappscore',
		'is_run': '是',
		'model': 'api',
		'level': 'P1',
		'desc': '',
		'domain': 'https://fast-test.mypaas.com',
		'api': '/api/appanalysis/641969597943123968/healthmetricscore/serverandappscore',
		'headers': {
			'envcode': 'prod',
			'x-fast-tenant': 'auto',
			'tenantcode': 'auto',
			'authorization': 'cc30e4e710c85b3f033d34d26bc06bbc02399bc9',
			'x-fast-user': 'pengda01',
			'x-fast-trace-id': 'fast-25575f287a0f620-0f820015a2-b3303153'
		},
		'cookies': '',
		'param': '$now',
		'body': '',
		'setup': {
			'type': 'func',
			'func': '${generate_overview_time_range(space=3600.0)}',
			'key': 'now_space'
		},
		'treandown': None,
		'extract_data': [{
			'type': 'response_body',
			'text': 'code=4000;msg=成功'
		}, {
			'type': 'response_code',
			'text': '200'
		}, {
			'type': 'response_body',
			'text': 'code=2000;msg=成功'
		}, {
			'type': 'response_code',
			'text': '400'
		}],
		'response': '',
		'black_list': ['a', 'b', 'c', 'd']
	}, {
		'case_id': 'case_04',
		'title': 'page_statistics',
		'is_run': '是',
		'model': 'api',
		'level': 'P1',
		'desc': '',
		'domain': 'https://fast-test.mypaas.com',
		'api': '/api/screen/641969597943123968/realtime/apphealth/page/statistics',
		'headers': {
			'envcode': 'prod',
			'x-fast-tenant': 'auto',
			'tenantcode': 'auto',
			'authorization': 'cc30e4e710c85b3f033d34d26bc06bbc02399bc9',
			'x-fast-user': 'pengda01',
			'x-fast-trace-id': 'fast-25575f287a0f620-0f820015a2-b3303153'
		},
		'cookies': '',
		'param': '$now',
		'body': '',
		'setup': [{
			'type': 'mysql',
			'database': 'api_test_starship_rbac',
			'sql': "select id as groups_id from rbac_group where name = 'CI组合场景自动化'",
			'key': 'groups_id'
		}, {
			'type': 'mysql',
			'database': 'api_test_starship_rbac',
			'sql': "select id as groups_id from rbac_group where name = 'CI组合场景自动化'"
		}],
		'treandown': None,
		'extract_data': [{
			'type': 'response_code',
			'text': '400'
		}, {
			'type': 'response_code',
			'text': '200'
		}, {
			'type': 'response_body',
			'text': 'code=2000;msg=成功'
		}],
		'response': '',
		'black_list': ['a', 'b', 'c', 'd']
	}, {
		'case_id': 'case_05',
		'title': 'realtime_abnormal_distribution',
		'is_run': '是',
		'model': 'api',
		'level': 'P1',
		'desc': '',
		'domain': 'https://fast-test.mypaas.com',
		'api': '/api/screen/641969597943123968/realtime/abnormal_distribution',
		'headers': {
			'envcode': 'prod',
			'x-fast-tenant': 'auto',
			'tenantcode': 'auto',
			'authorization': 'cc30e4e710c85b3f033d34d26bc06bbc02399bc9',
			'x-fast-user': 'pengda01',
			'x-fast-trace-id': 'fast-25575f287a36740-7274006f56-cd204d36'
		},
		'cookies': '',
		'param': '$now',
		'body': '',
		'setup': None,
		'treandown': [{
			'type': 'mysql',
			'database': 'api_test_starship_rbac',
			'sql': "select id as groups_id from rbac_group where name = 'CI组合场景自动化'",
			'key': 'groups_id'
		}, {
			'type': 'mysql',
			'database': 'api_test_starship_rbac',
			'sql': "select id as groups_id from rbac_group where name = 'CI组合场景自动化'"
		}, {
			'type': 'mysql',
			'database': 'api_test_starship_rbac',
			'sql': "select id as groups_id from rbac_group where name = '我是测试数据'"
		}],
		'extract_data': [{
			'type': 'response_code',
			'text': '400'
		}, {
			'type': 'response_code',
			'text': '200'
		}, {
			'type': 'response_body',
			'text': 'code=2000;msg=成功'
		}],
		'response': '',
		'black_list': ['a', 'b', 'c', 'd']
	}, {
		'case_id': 'case_06',
		'title': 'realtime_flow',
		'is_run': '是',
		'model': 'api',
		'level': 'P1',
		'desc': '',
		'domain': 'https://fast-test.mypaas.com',
		'api': '/api/screen/641969597943123968/realtime/flow',
		'headers': {
			'envcode': 'prod',
			'x-fast-tenant': 'auto',
			'tenantcode': 'auto',
			'authorization': 'cc30e4e710c85b3f033d34d26bc06bbc02399bc9',
			'x-fast-user': 'pengda01',
			'x-fast-trace-id': 'fast-25575f287a4c6c0-14ec00f3c8-882f472f'
		},
		'cookies': '',
		'param': '$now_space',
		'body': '',
		'setup': {
			'type': 'func',
			'func': '${generate_overview_time_range(space=3600)}',
			'key': 'now_space'
		},
		'treandown': None,
		'extract_data': [{
			'type': 'response_code',
			'text': '400'
		}, {
			'type': 'response_code',
			'text': '200'
		}, {
			'type': 'response_body',
			'text': 'code=2000;msg=成功'
		}],
		'response': '',
		'black_list': ['a', 'b', 'c', 'd']
	}, {
		'case_id': 'case_07',
		'title': 'realtime_mks_events',
		'is_run': '是',
		'model': 'api',
		'level': 'P1',
		'desc': '',
		'domain': 'https://fast-test.mypaas.com',
		'api': '/api/screen/641969597943123968/realtime/mks_events',
		'headers': {
			'envcode': 'prod',
			'x-fast-tenant': 'auto',
			'tenantcode': 'auto',
			'authorization': 'cc30e4e710c85b3f033d34d26bc06bbc02399bc9',
			'x-fast-user': 'pengda01',
			'x-fast-trace-id': 'fast-25575f287a62660-bc46000b3f-e1414b6d'
		},
		'cookies': '',
		'param': '$now_page',
		'body': '',
		'setup': {
			'type': 'func',
			'func': '${generate_overview_time_range(page=1)}',
			'key': 'now_page'
		},
		'treandown': None,
		'extract_data': [{
			'type': 'response_code',
			'text': '400'
		}, {
			'type': 'response_code',
			'text': '200'
		}, {
			'type': 'response_body',
			'text': 'code=2000;msg=成功'
		}],
		'response': '',
		'black_list': ['a', 'b', 'c', 'd']
	}, {
		'case_id': 'case_08',
		'title': 'metric-proxy_',
		'is_run': '是',
		'model': 'api',
		'level': 'P1',
		'desc': '',
		'domain': 'https://fast-test.mypaas.com',
		'api': '/api/metric-proxy/',
		'headers': {
			'envcode': 'prod',
			'x-fast-tenant': 'auto',
			'tenantcode': 'auto',
			'authorization': 'cc30e4e710c85b3f033d34d26bc06bbc02399bc9',
			'x-fast-user': 'pengda01',
			'x-fast-trace-id': 'fast-25575f287a22ec0-c36c00455c-ed696533'
		},
		'cookies': '',
		'param': {
			'dashboard_type': '6',
			'product_id': '641969597943123968',
			'mks_env_tag': 'prod'
		},
		'body': '',
		'setup': None,
		'treandown': None,
		'extract_data': [{
			'type': 'response_code',
			'text': '200'
		}, {
			'type': 'response_code',
			'text': '400'
		}, {
			'type': 'response_body',
			'text': 'code=4000;msg=未能获取到基础监控数据，请与容器云（天眼）确认是否已配置采集应用基础监控信息'
		}],
		'response': '',
		'black_list': ['a', 'b', 'c', 'd']
	}]
} 

print(json.dumps(data,ensure_ascii=False))