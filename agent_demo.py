from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import math

API_KEY = "453c357c4c994eefab41ba9c15cf7060.D30xZ8FtxTaEl7t8" # ⚠️ 记得换成你自己的 Key
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

# 1. 初始化大模型
llm = ChatOpenAI(model="glm-4-flash", api_key=API_KEY, base_url=BASE_URL)

# 2. 定义工具一：计算器
@tool
def calculate(expression: str) -> str:
    """当你需要进行数学计算时，请使用此工具。输入应该是一个合法的 Python 数学表达式，比如 '2 + 2' 或 'math.sqrt(16)'"""
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"

# 3. 定义工具二：本地知识库（模拟查数据库）
@tool
def lzu_info(query: str) -> str:
    """当你需要查询兰州大学大模型社团的内部信息时，请使用此工具。输入关键词可以是'导师'、'办公室'或'大一要求'。"""
    if "导师" in query or "老师" in query:
        return "大模型社团的指导老师姓王。"
    elif "办公室" in query:
        return "王老师的办公室在信息楼302。"
    elif "大一" in query or "要求" in query:
        return "大一新生每周需要保证10个小时的AI学习时间。"
    else:
        return "没有找到相关的内部信息。"

# 把工具装进工具箱
tools = [calculate, lzu_info]

# 4. 设定 AI 的系统提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个全能的 AI 助手。你可以使用工具来帮助用户解决问题。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 5. 创建 Agent（智能体）
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 6. 开始测试
print("=== 你的专属 AI 智能体已上线 ===")
while True:
    user_q = input("\n你问：")
    if user_q == "退出":
        break
    
    print("AI 正在思考并调用工具...")
    response = agent_executor.invoke({"input": user_q})
    print(f"\nAI 最终回答：{response['output']}")
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import math

API_KEY = "453c357c4c994eefab41ba9c15cf7060.D30xZ8FtxTaEl7t8" # ⚠️ 记得换成你自己的 Key
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

# 1. 初始化大模型
llm = ChatOpenAI(model="glm-4-flash", api_key=API_KEY, base_url=BASE_URL)

# 2. 定义工具一：计算器
@tool
def calculate(expression: str) -> str:
    """当你需要进行数学计算时，请使用此工具。输入应该是一个合法的 Python 数学表达式，比如 '2 + 2' 或 'math.sqrt(16)'"""
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"

# 3. 定义工具二：本地知识库（模拟查数据库）
@tool
def lzu_info(query: str) -> str:
    """当你需要查询兰州大学大模型社团的内部信息时，请使用此工具。输入关键词可以是'导师'、'办公室'或'大一要求'。"""
    if "导师" in query or "老师" in query:
        return "大模型社团的指导老师姓王。"
    elif "办公室" in query:
        return "王老师的办公室在信息楼302。"
    elif "大一" in query or "要求" in query:
        return "大一新生每周需要保证10个小时的AI学习时间。"
    else:
        return "没有找到相关的内部信息。"

# 把工具装进工具箱
tools = [calculate, lzu_info]

# 4. 设定 AI 的系统提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个全能的 AI 助手。你可以使用工具来帮助用户解决问题。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 5. 创建 Agent（智能体）
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 6. 开始测试
print("=== 你的专属 AI 智能体已上线 ===")
while True:
    user_q = input("\n你问：")
    if user_q == "退出":
        break
    
    print("AI 正在思考并调用工具...")
    response = agent_executor.invoke({"input": user_q})
    print(f"\nAI 最终回答：{response['output']}")