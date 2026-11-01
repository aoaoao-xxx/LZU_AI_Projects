import gradio as gr
import requests  # 新增：用于发送网络请求
import math
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# 1. 配置大模型
API_KEY = "453c357c4c994eefab41ba9c15cf7060.D30xZ8FtxTaEl7t8"  # ⚠️ 换成你自己的
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

llm = ChatOpenAI(model="glm-4-flash", api_key=API_KEY, base_url=BASE_URL)

# 2. 定义工具一：计算器
@tool
def calculate(expression: str) -> str:
    """当你需要进行数学计算时，请使用此工具。"""
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"

# 3. 定义工具二：本地知识库
@tool
def lzu_info(query: str) -> str:
    """当你需要查询兰州大学大模型社团的内部信息时（如导师、办公室、大一要求），请使用此工具。"""
    if "导师" in query or "老师" in query:
        return "大模型社团的指导老师姓王。"
    elif "办公室" in query:
        return "王老师的办公室在信息楼302。"
    elif "大一" in query or "要求" in query:
        return "大一新生每周需要保证10个小时的AI学习时间。"
    else:
        return "没有找到相关的内部信息。"

# 4. 定义工具三：查天气
# 把原来的 get_weather 函数替换成这样：
@tool
def get_weather(city: str) -> str:
    """当用户需要查询天气时，请使用此工具。"""
    try:
        # 核心知识点：用 with open 读取本地文件
        with open("weather.txt", "r", encoding="utf-8") as f:
            weather_info = f.read()
        return weather_info
    except FileNotFoundError:
        return "抱歉，本地没有找到天气数据文件。"

# 5. 把三个工具装进工具箱
tools = [calculate, lzu_info, get_weather]

# 6. 设定 AI 的系统提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个全能的 AI 助手。你可以使用工具来帮助用户解决问题。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 7. 创建 Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

# 8. 网页聊天函数
def chat_with_agent(message, history):
    response = agent_executor.invoke({"input": message})
    return response["output"]

# 9. 网页界面
demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="全能 Agent 助手",
    description="支持数学计算、社团信息查询与天气查询"
)

# 10. 启动
demo.launch()