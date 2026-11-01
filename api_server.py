from fastapi import FastAPI
from pydantic import BaseModel
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import math

# 1. 初始化 FastAPI 应用
app = FastAPI(title="LZU AI Agent API")

# 2. 初始化大模型和工具（跟之前一模一样）
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
    if "办公室" in query:
        return "王老师的办公室在信息楼302。"
    elif "导师" in query or "老师" in query:
        return "大模型社团的指导老师姓王。"
    elif "大一" in query or "要求" in query:
        return "大一新生每周需要保证10个小时的AI学习时间。"
    else:
        return "没有找到相关的内部信息。"

tools = [calculate, lzu_info]
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个全能的 AI 助手。必须优先调用工具查询，不要自己瞎猜。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 3. 核心重点：定义数据格式 (Pydantic)
# 规定前端发过来的数据必须包含一个 question 字段，且必须是字符串
class ChatRequest(BaseModel):
    question: str

# 4. 定义一个 POST 接口
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # 接收到前端发来的问题
    user_question = request.question
    
    # 交给 Agent 处理
    response = agent_executor.invoke({"input": user_question})
    
    # 把结果打包成 JSON 返回给前端
    return {"answer": response["output"]}