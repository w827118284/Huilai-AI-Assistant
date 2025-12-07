#sk-1dd3d9aa14a14c8996afd6d9a74e2bad
from openai import OpenAI

# 1. 配置“电话拨号盘”
# 这里的 base_url 就是告诉代码：别打给美国，打给 DeepSeek 的服务器
client = OpenAI(
    api_key="sk-1dd3d9aa14a14c8996afd6d9a74e2bad",  # 👈 记得换成你的 Key
    base_url="https://api.deepseek.com"
)

print("正在呼叫 DeepSeek，请稍等...")

# 2. 发送指令
# model="deepseek-chat" 是指名点姓要用它的 V3 模型
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "你好，我是计算机专业研一新生，请用一句最有哲理的话鼓励我学习Python。"}
    ]
)

# 3. 打印它的回复
print("DeepSeek 回复说：")
# 这是一个典型的“剥洋葱”操作（还记得刚才学的字典吗？）
print(response.choices[0].message.content)