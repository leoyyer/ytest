# 运行模式

- 运行整个文件夹的用例
  - ytest run project
  - ytest run project file
- 运行单个用例
  - ytest run excel 的绝对路径
- debug 用例

  - 选中 excel 直接点运行

- debug 用例需要配置 launch.json

```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "debug case",
      "type": "python",
      "request": "launch",
      "cwd": "${workspaceFolder}",
      "env": {},
      "envFile": "${workspaceFolder}/.venv",
      "console": "integratedTerminal",
      "program": "${workspaceFolder}/ytest/utils/case/test_default_case.py",
      "args": ["--filename", "${file}"]
    },
    {
      "name": "Python: 当前文件",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}

```

- 其他调试模式
  ytest/utils/case/test_default_case.py --filename case/fast/suite/fast_app_product_screen.xlsx

-- 调试
本地打包:
pip install -e .

✗ ytest run -p fast -t api --env test -f fast_auto_product_screen_1

pip install git+https://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:x-oauth-basic@github.com/leoyyer/ytest.git \
 --index-url https://mirrors.aliyun.com/pypi/simple \
 --no-build-isolation
