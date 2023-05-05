import jsonschema
from jsonschema import generate_schema
import json

# 定义要检查的数据
data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# 生成JSON Schema
schema = generate_schema(data)

# 将JSON Schema保存到文件
with open('json_schema.json', 'w') as f:
    jsonschema.validators.Draft7Validator.check_schema(schema)
    json.dump(schema, f, indent=4)
