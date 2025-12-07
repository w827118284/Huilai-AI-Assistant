
import os
import streamlit as st
import httpx # 必须导入这个
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

# ==========================================
# 👇 1. 基础配置
# ==========================================
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
st.set_page_config(page_title="huilai的智能研报助手", page_icon="🤖", layout="wide")

# ==========================================
# 👇 2. 填入 Key (请检查你的 Key 是否正确！)
# ==========================================
DEEPSEEK_API_KEY = "sk-1dd3d9aa14a14c8996afd6d9a74e2bad"
ZHIPUAI_API_KEY = "bfdb8628746c49849fb4eb767cfa9d07.RFuOavDnbMjGVnT9"
# ==========================================

# 临时文件夹
if not os.path.exists("./temp"):
    os.makedirs("./temp")

# ==========================================
# 👇 3. 核心功能：处理上传文件
# ==========================================
def process_uploaded_file(uploaded_file):
    file_path = os.path.join("./temp", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    
    embedding_model = ZhipuAIEmbeddings(model="embedding-2", api_key=ZHIPUAI_API_KEY)
    
    # 强制重新创建数据库
    vector_db = Chroma.from_documents(
        documents=splits,
        embedding=embedding_model,
        persist_directory="./chroma_db"
    )
    return vector_db

# ==========================================
# 👇 4. 核心功能：加载链 (Day 2 记忆版)
# ==========================================
@st.cache_resource
def load_chain():
    # A. 加载 Embedding
    embedding_model = ZhipuAIEmbeddings(model="embedding-2", api_key=ZHIPUAI_API_KEY)
    
    # B. 检查数据库
    if not os.path.exists("./chroma_db"):
        return None
        
    db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)
    
    # C. 加载大模型 (低温严谨)
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",
        temperature=0.1
    )
    
    # D. 定义人设 Prompt
    template = """
    你是一名专业的 AI 研报分析助手，你的名字叫“会来”。
    请严格根据以下【参考文档】的内容回答用户的【问题】。
    
    【回答规则】：
    1. 语气要专业、严谨。
    2. 严禁瞎编，找不到答案就说不知道。
    3. 回答最后，请加上一句：“—— 由会来的 AI 助手生成”。

    【参考文档】：
    {context}

    【用户问题】：
    {question}

    请开始分析并回答：
    """
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # E. 定义记忆 Memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # F. 组装对话链 (注意：这里用的是 ConversationalRetrievalChain)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    return qa_chain

# ==========================================
# 👇 5. 界面 UI
# ==========================================
st.title("🤖 huilai的智能研报助手")

# --- 侧边栏 ---
with st.sidebar:
    st.header("📄 文档上传")
    uploaded_file = st.file_uploader("请上传 PDF 文件", type=["pdf"])
    
    if uploaded_file:
        if st.button("开始分析"):
            with st.spinner("正在拆解文档，请稍等..."):
                try:
                    process_uploaded_file(uploaded_file)
                    st.success("✅ 分析完成！数据库已更新。")
                    # 清空历史，防止串台
                    st.session_state["messages"] = [{"role": "assistant", "content": "你好！新文档已加载，请问吧！"}]
                    st.cache_resource.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"处理失败: {e}")

# --- 主界面聊天 ---
chain = load_chain()

if not chain:
    st.warning("👈 请先在左侧上传一个 PDF 文档，点击“开始分析”！")
else:
    # 初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "你好！我已经准备好回答关于这份文档的问题了。"}]

    # 显示历史消息
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    # 处理用户输入
    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        st.session_state["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("AI 正在回忆并思考..."):
                try:
                    # 👇 关键点：这里必须用 "question"，绝对不能用 "query"
                    response = chain.invoke({"question": prompt})
                    
                    # 👇 关键点：结果在 "answer" 里
                    result = response["answer"]
                    
                    st.write(result)
                    st.session_state["messages"].append({"role": "assistant", "content": result})
                except Exception as e:
                    st.error(f"生成回答时出错: {e}")