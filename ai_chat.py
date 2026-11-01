from openai import OpenAI

# 1. 告诉代码：你要用谁家的服务，你的密码是什么
client = OpenAI(
    api_key="453c357c4c994eefab41ba9c15cf7060.D30xZ8FtxTaEl7t8", # ⚠️ 注意保留两边的英文双引号，把里面的字换掉
    base_url="https://open.bigmodel.cn/api/paas/v4/" # 这是智谱的专属网址
)

print("AI 已就绪，输入 '退出' 结束对话。")

# 2. 我们用一个死循环，让你可以一直跟它聊天
while True:
    # 接收你的输入
    user_input = input("\n你：")
    
    # 如果输入的是“退出”，就打破循环，结束程序
    if user_input == "退出":
        print("再见！")
        break
    
    # 3. 把你说的话，发送给大模型
    print("AI 正在思考中...")
    response = client.chat.completions.create(
        model="glm-4-flash", # 这是智谱目前免费且速度极快的模型
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    
    # 4. 把大模型的回复提取出来，打印在屏幕上
    ai_reply = response.choices[0].message.content
    print(f"AI：{ai_reply}")