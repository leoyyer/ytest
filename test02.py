from transformers import pipeline

# 加载预训练模型
nlg = pipeline("text-generation", model="gpt-3.5-turbo")  # 替换为具体的模型

# 定义生成模板和输入数据
template = (
    "当用户 {username} 使用密码 {password} 登录时，系统应该 {expected_behavior}。"
)
inputs = {"username": "admin", "password": "pass123", "expected_behavior": "成功登录"}
prompt = template.format(**inputs)

# 生成测试用例
results = nlg(prompt, max_length=50)
print(results[0]["generated_text"])
