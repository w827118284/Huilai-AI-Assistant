import os
# ==========================================
# 👇 还是老规矩，清空代理，保证网络通畅
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
# ==========================================

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# ==========================================
# 🔑 请填入你的两个 Key
# 1. DeepSeek 的 Key (用于回答问题)
DEEPSEEK_API_KEY = "sk-1dd3d9aa14a14c8996afd6d9a74e2bad"
# 2. 智谱的 Key (用于去数据库搜东西，跟上一步保持一致)
ZHIPUAI_API_KEY = "bfdb8628746c49849fb4eb767cfa9d07.RFuOavDnbMjGVnT9"
# ==========================================

# 1. 加载刚才建好的数据库 (记忆)
print("1. 正在加载数据库...")
embedding_model = ZhipuAIEmbeddings(
    model="embedding-2",
    api_key=ZHIPUAI_API_KEY
)
# 这里的 persist_directory 必须和上一步 create_db.py 里写的一模一样
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)

# 2. 召唤 DeepSeek 大模型 (大脑)
print("2. 正在连接 DeepSeek...")
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    temperature=0.3  # 数值越低，回答越严谨，越依靠文档
)

# 3. 组装流水线 (Chain)
# 这行代码的意思是：创建一个检索问答链，使用 llm 作为大脑，db作为检索源
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", # stuff = 把搜到的资料一股脑塞给 AI
    retriever=db.as_retriever(search_kwargs={"k": 3}) # k=3 意思是只找最相关的 3 段话
)

# 4. 开始提问！
print("\n" + "="*30)
print("🤖 你的专属 AI 知识助手已上线！")
print("   (输入 'quit' 或 'exit' 退出)")
print("="*30)

while True:
    # 让用户输入问题
    query = input("\n请根据 PDF 提问: ")
    
    if query.lower() in ["quit", "exit"]:
        print("拜拜！")
        break
    
    print("Thinking...")
    # 核心调用：让 AI 根据文档回答
    try:
        # invoke 是 LangChain 运行链的标准指令
        response = qa_chain.invoke({"query": query})
        print("\n✅ AI 回答：")
        print(response["result"]) # 打印出结果
    except Exception as e:
        print(f"❌ 出错啦: {e}")