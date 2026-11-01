import gradio as gr
from langchain_community.document_loaders import PyPDFLoader # 换成PDF加载器
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate

API_KEY = "453c357c4c994eefab41ba9c15cf7060.D30xZ8FtxTaEl7t8"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

llm = ChatOpenAI(model="glm-4-flash", api_key=API_KEY, base_url=BASE_URL)
embeddings = OpenAIEmbeddings(model="embedding-2", api_key=API_KEY, base_url=BASE_URL)

# 1. 初始化 PDF 知识库
print("正在解析 PDF 并建立向量数据库，请稍候...")
# 这里的 "test.pdf" 换成你实际的文件名
loader = PyPDFLoader("test.pdf") 
documents = loader.load()

# PDF 的字数很大，必须按段落切分，这里按 500 个字符切
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2}) # 找出最相关的2段
print("✅ PDF 知识库已就绪！")

# 2. 聊天函数
def chat_with_pdf(message, history):
    # 检索相关的 PDF 片段
    context_docs = retriever.invoke(message)
    context = "\n\n".join([doc.page_content for doc in context_docs])
    
    prompt = f"""
    你是一个文档分析助手。请严格根据下面的参考资料回答用户问题。
    如果资料里没有，请直接回答“根据现有资料，我无法回答这个问题”。
    
    【参考资料】：
    {context}
    
    【用户问题】：
    {message}
    """
    
    # 3. 关键改动：这里用 llm.stream 开启流式输出
    # 这段代码会让网页一个字一个字往外蹦，体验极佳
    response = llm.invoke(prompt)
    return response.content

# 4. 网页界面
demo = gr.ChatInterface(
    fn=chat_with_pdf,
    title="PDF 智能文档分析助手",
    description="上传 PDF 并基于内容进行问答"
)

demo.launch()