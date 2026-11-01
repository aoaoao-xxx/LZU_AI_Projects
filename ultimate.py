import gradio as gr
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os

API_KEY = "453c357c4c994eefab41ba9c15cf7060.D30xZ8FtxTaEl7t8"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

llm = ChatOpenAI(model="glm-4-flash", api_key=API_KEY, base_url=BASE_URL)
embeddings = OpenAIEmbeddings(model="embedding-2", api_key=API_KEY, base_url=BASE_URL)

# 全局变量，用来存当前的检索器
global_retriever = None

# 1. 处理 PDF 上传的函数
def process_pdf(file):
    global global_retriever
    if file is None:
        return "⚠️ 请先上传一个 PDF 文件"
    
    try:
        # Gradio 上传的 file 是一个临时文件对象，我们用 file.name 获取路径
        loader = PyPDFLoader(file.name)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)
        
        vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
        global_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
        
        return f"✅ PDF 解析成功！已提取 {len(docs)} 个文本块，可以开始提问了。"
    except Exception as e:
        return f"❌ 解析失败：{str(e)}"

# 2. 聊天函数（带记忆 + RAG）
def chat_with_pdf(message, history):
    global global_retriever
    
    if global_retriever is None:
        return "⚠️ 请先在左侧上传 PDF 文件！"
    
    # RAG 检索
    context_docs = global_retriever.invoke(message)
    context = "\n\n".join([doc.page_content for doc in context_docs])
    
    # 组装带上历史的 Prompt
    prompt = f"""
    你是一个文档分析助手。请严格根据下面的参考资料回答用户问题。
    如果资料里没有，请直接回答“根据现有资料，我无法回答这个问题”。
    
    【参考资料】：
    {context}
    
    【用户问题】：
    {message}
    """
    
    # 为了演示方便，这里暂时只把当前问题+检索内容发给大模型（RAG专用的单轮问答）
    # 实际企业开发中，这里会把 history 也拼进去
    response = llm.invoke(prompt)
    return response.content

# 3. 构建高级 UI 布局
with gr.Blocks(title="PDF 智能问答") as demo:
    gr.Markdown("## 📄 企业级 PDF 智能分析助手")
    gr.Markdown("上传 PDF 文件，AI 会根据文档内容为你解答。")
    
    with gr.Row():
        # 左侧：上传区
        with gr.Column(scale=1):
            file_input = gr.File(label="上传 PDF 文件", file_types=[".pdf"])
            upload_btn = gr.Button("解析文档", variant="primary")
            status_text = gr.Textbox(label="系统状态", value="等待上传...", interactive=False)
            
        # 右侧：聊天区
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(label="对话记录")
            msg = gr.Textbox(label="输入你的问题", placeholder="例如：这篇文档讲了什么？")
            with gr.Row():
                submit_btn = gr.Button("发送")
                clear_btn = gr.Button("清空对话")

    # 4. 绑定事件
    # 上传按钮点击 -> 运行 process_pdf -> 更新状态框
    upload_btn.click(process_pdf, inputs=[file_input], outputs=[status_text])
    
    # 发送消息 -> 发送到聊天框（注意：Gradio 新版处理聊天记录的方法）
        # ================= 替换这里开始 =================
    # 发送消息 -> 发送到聊天框（适配最新版 Gradio 的字典格式）
        # 4. 绑定事件
    # 上传按钮点击
    upload_btn.click(process_pdf, inputs=[file_input], outputs=[status_text])
    
    # 发送消息的核心处理函数（融合了输入、调用API、更新UI）
    def respond(message, chat_history):
        if not message.strip():
            return "", chat_history
            
        # 调用你写好的 RAG 问答函数
        bot_message = chat_with_pdf(message, chat_history)
        
        # 把用户说的话和 AI 说的话一起加到聊天记录里
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_message})
        
        # 清空输入框，返回更新后的聊天记录
        return "", chat_history

    # 绑定发送按钮和回车键
    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    
    # 清空按钮
    clear_btn.click(lambda: None, None, chatbot, queue=False)

# 启动
demo.launch()