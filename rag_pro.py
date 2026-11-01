from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 1. 初始化大模型和向量化模型（智谱的配置）
API_KEY = "453c357c4c994eefab41ba9c15cf7060.D30xZ8FtxTaEl7t8"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

llm = ChatOpenAI(
    model="glm-4-flash",
    api_key=API_KEY,
    base_url=BASE_URL
)

# 智谱的向量化模型（把文字变成数字，方便算相似度）
embeddings = OpenAIEmbeddings(
    model="embedding-2", 
    api_key=API_KEY,
    base_url=BASE_URL
)

def setup_rag():
    print("正在加载本地知识库...")
    # 2. 读取文件并切分（RAG的核心：切成小块）
    loader = TextLoader("knowledge.txt", encoding="utf-8")
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    
    # 3. 存入向量数据库（这里会自动计算语义相似度）
    print("正在建立向量数据库...")
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
    
    # 4. 真正的语义检索器
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    return retriever

retriever = setup_rag()
print("✅ 知识库已就绪！可以开始提问了。")

# 5. 开始对话
while True:
    question = input("\n你问：")
    if question == "退出":
        break
    
    print("AI正在查阅资料...")
    # 语义检索：找出最相关的一段话
    context_docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in context_docs])
    
    # 拼装 Prompt
    prompt = f"""
    你是一个校园智能助手。请严格根据下面的参考资料回答用户问题。
    如果资料里没有，请直接回答“根据现有资料，我无法回答这个问题”。
    请用傲娇的语气回答
    【参考资料】：{context}
    【用户问题】：{question}
    """
    
    # 发给大模型
    response = llm.invoke(prompt)
    print(f"AI：{response.content}")