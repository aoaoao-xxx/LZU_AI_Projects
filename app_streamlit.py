import streamlit as st
import math
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# ================= 1. 页面基础设置 =================
# 设置网页标题、图标和宽屏模式
st.set_page_config(page_title="全能 Agent 助手", page_icon="🤖", layout="wide")

# ================= 2. 初始化 Agent =================
API_KEY = "453c357c4c994eefab41ba9c15cf7060.D30xZ8FtxTaEl7t8" # ⚠️ 换成你的
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"
llm = ChatOpenAI(model="glm-4-flash", api_key=API_KEY, base_url=BASE_URL)

@tool
def calculate(expression: str) -> str:
    """当你需要进行数学计算时，请使用此工具。"""
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"

@tool
def lzu_info(query: str) -> str:
    """当用户询问关于‘王老师’、‘大模型社团导师’、‘社团办公室’或‘大一新生要求’等信息时，必须使用此工具。"""
    if "导师" in query or "老师" in query:
        return "大模型社团的指导老师姓王。"
    elif "办公室" in query:
        return "王老师的办公室在信息楼302。"
    elif "大一" in query or "要求" in query:
        return "大一新生每周需要保证10个小时的AI学习时间。"
    else:
        return "没有找到相关的内部信息。"

tools = [calculate, lzu_info]
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个全能助手。只要用户问到了‘老师’、‘办公室’、‘社团’，你必须优先调用相关工具查询，不要自己瞎猜。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ================= 3. 构建网页界面 =================

# 左侧边栏
with st.sidebar:
    st.header("⚙️ 控制面板")
    st.markdown("这是一个基于 LangChain 和 Streamlit 构建的全能智能体。")
    st.markdown("**功能清单：**\n- 📊 数学计算\n- 🏫 兰大社团信息查询")
    # 加个清空按钮
    if st.button("🗑️ 清空聊天记录"):
        st.session_state.messages = []
        st.rerun()

# 主界面标题
st.title("🤖 全能 Agent 助手")
st.caption("支持数学计算与社团信息查询")

# 核心重点：Streamlit 的状态管理 (Session State)
# 网页每次刷新都会重跑代码，必须用 st.session_state 才能记住聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 把历史聊天记录渲染到屏幕上
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用户输入
if user_input := st.chat_input("请输入你的问题..."):
    # 1. 把用户的话显示在屏幕上并存入记忆
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 2. AI 开始思考并回答
    with st.chat_message("assistant"):
        with st.spinner("AI 正在思考并调用工具..."):
            # 调用你的 Agent
            response = agent_executor.invoke({"input": user_input})
            answer = response["output"]
            # 显示 AI 的回答
            st.markdown(answer)
            # 存入记忆
            st.session_state.messages.append({"role": "assistant", "content": answer})