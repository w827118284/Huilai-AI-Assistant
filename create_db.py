import os
# 清空代理，防止报错
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import ZhipuAIEmbeddings

# ==========================================
# 👇 填入你刚才申请的智谱 API Key
ZHIPUAI_API_KEY = "bfdb8628746c49849fb4eb767cfa9d07.RFuOavDnbMjGVnT9"
# ==========================================

print("1. 读取 PDF...")
# 记得用你刚才成功的那个绝对路径！
loader = PyPDFLoader(r"C:\Users\huilai\Desktop\data.pdf")
docs = loader.load()

print("2. 切分文档...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

print(f"3. 正在调用智谱AI，把 {len(splits)} 个片段存入向量数据库...")
print("   (这一步需要联网，可能会花几十秒，请耐心等待...)")

# 定义嵌入模型
embedding_model = ZhipuAIEmbeddings(
    model="embedding-2", # 智谱的通用模型
    api_key=ZHIPUAI_API_KEY
)

# 创建并保存向量数据库
# persist_directory 就是数据库在硬盘上的文件夹名字
vector_db = Chroma.from_documents(
    documents=splits,
    embedding=embedding_model,
    persist_directory="./chroma_db" 
)

print("✅ 成功！数据已存入 'chroma_db' 文件夹。")