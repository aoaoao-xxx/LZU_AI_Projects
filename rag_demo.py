from openai import OpenAI

client = OpenAI(
    api_key="你的API_KEY填在这里", 
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

def ask_with_rag(question):
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge_lines = f.readlines()

    # 1. 真正的检索 (Retrieval)：找出包含问题中某些字的句子
    # 比如问题里包含“王老师”，就把带有“王老师”的那行挑出来
    relevant_chunks = []
    for line in knowledge_lines:
        # 极简版：如果问题里的字（或者问题本身）出现在这句话里，就选它
        # (在真实企业里，这里是计算“向量相似度”)
        if question in line or any(char in line for char in question if len(char) > 0):
            relevant_chunks.append(line)
    
    # 把选出来的段落拼起来
    context = "".join(relevant_chunks)
    
    # 如果没检索到相关内容，直接返回
    if not context.strip():
        return "根据现有资料，我无法回答这个问题。"

    # 2. 增强 (Augmentation)：把检索到的局部内容拼给 AI
    prompt = f"""
    你是一个校园智能助手。请严格根据下面提供的【参考资料】来回答问题。
    如果资料里没有，请直接回答“根据现有资料，我无法回答这个问题”。

    【参考资料】：
    {context}

    【用户问题】：
    {question}
    """

    # 3. 生成 (Generation)
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

print("=== 升级版 RAG 助手（带精准检索） ===")
while True:
    user_q = input("\n请输入你的问题（输入'退出'结束）：")
    if user_q == "退出":
        break
    
    print("AI正在检索知识库...")
    answer = ask_with_rag(user_q)
    print(f"\nAI回答：{answer}")