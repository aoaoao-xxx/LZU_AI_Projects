import gradio as gr
from openai import OpenAI

# 1. 填入你的 API Key
client = OpenAI(
    api_key="453c357c4c994eefab41ba9c15cf7060.D30xZ8FtxTaEl7t8", 
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

# 2. 这个函数负责和 AI 交流，并且带有“记忆”功能
def chat_with_ai(message, history):
    # 最新版 Gradio 的 history 已经直接是标准的对话格式了，直接用！
    messages = history + [{"role": "user", "content": message}]
    
    # 发送请求
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=messages
    )
    return response.choices[0].message.content

# 3. 一行代码生成网页聊天框
demo = gr.ChatInterface(
    fn=chat_with_ai, 
    title="我的第一个 AI 助手",
    description="这是由兰大大一新生独立开发的网页版 AI"
)

# 4. 启动网页
demo.launch(share=True)