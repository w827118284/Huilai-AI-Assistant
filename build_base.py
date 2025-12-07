import os
# ==========================================
# 👇 还是先清空代理，防止网络报错
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
# ==========================================

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 1. 设置 Key (这里我们要用 DeepSeek 或者是通用的 Embedding)
# ⚠️ 注意：DeepSeek 目前主要提供对话，Embedding 有时候不稳定。
# 为了稳妥，我们这里先尝试用一个开源的、不需要Key的本地模型，或者
# 如果你有 OpenAI 的 Key 可以用 OpenAI。
# 这里我们暂时演示“读取+切割”的流程，先不调用 API，确保基本功扎实。

print("1. 正在读取 PDF 文件...")
# 确保你的桌面上有一个叫 data.pdf 的文件
loader = PyPDFLoader(r"C:\Users\huilai\Desktop\data.pdf")
docs = loader.load()
print(f"   成功读取，这篇文档一共有 {len(docs)} 页。")

print("2. 正在切分文档...")
# 为什么要切分？因为大模型一次吃不下整本书，要切成小块（Chunk）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,    # 每一块大约 500 个字
    chunk_overlap=50   # 前后重叠 50 个字（防止句子被切断）
)
splits = text_splitter.split_documents(docs)
print(f"   切分完成！原文档被切成了 {len(splits)} 个小块。")

print("3. 看看切出来的第一块长什么样：")
print("-" * 30)
print(splits[0].page_content)
print("-" * 30)

print("🎉 恭喜！数据预处理流程跑通了！")