
import json
# 定义模板
from typing import List, Dict, Any, Optional

import yaml
import json
from jsonschema import validate

# 读取 YAML 文件
with open("data/fast/suite/demo/demo02.yaml", "r") as f:
    yaml_data = yaml.safe_load(f)

# 读取 JSON Schema 文件
with open("ytest/utils/templates/json_schema.json", "r") as f:
    json_schema = json.load(f)

# 验证 YAML 数据是否符合 JSON Schema
validate(instance=yaml_data, schema=json_schema)

# 将 Python 字典转换为 JSON 字符串
json_data = json.dumps(yaml_data,ensure_ascii=False)

# 将 JSON 字符串写入文件
with open("your.json", "w") as f:
    f.write(json_data)
