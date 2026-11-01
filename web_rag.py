import gradio as gr
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# 1. 配置大模型
API_KEY = "453c357c4c994eefab41ba9c15cf7060.D30xZ8FtxTaEl7t8"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

llm = ChatOpenAI(model="glm-4-flash", api_key=API_KEY, base_url=BASE_URL)
embeddings = OpenAIEmbeddings(model="embedding-2", api_key=API_KEY, base_url=BASE_URL)

# 2. 启动时加载知识库（这部分和你刚才跑的一样）
print("正在初始化知识库...")
loader = TextLoader("knowledge.txt", encoding="utf-8")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
print("✅ 知识库已就绪！")

# 3. 网页聊天的核心函数
def chat_with_rag(message, history):
    # 去知识库里检索
    context_docs = retriever.invoke(message)
    context = "\n".join([doc.page_content for doc in context_docs])
    
    # 组装 Prompt
    prompt = f"""
    你是一个校园智能助手。请严格根据下面的参考资料回答用户问题。
    如果资料里没有，请直接回答“根据现有资料，我无法回答这个问题”。
    请用撒娇的语气回答
    
    【参考资料】：{context}
    【用户问题】：{message}
    """
    
    # 发给大模型获取回答
    response = llm.invoke(prompt)
    return response.content

# 4. 生成网页界面
demo = gr.ChatInterface(
    fn=chat_with_rag,
    title="校园专属 RAG 知识库",
    description="由兰大大一新生独立开发，支持本地知识库检索"
)

# 5. 启动网页
demo.launch()