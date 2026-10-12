import os
from src.chunkers import load_documents, heading_chunk
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def build_vectorstore():
    print("1. 正在加载文档并切块...")
    docs = load_documents("data/raw")
    chunks = heading_chunk(docs)
    
    print("2. 正在加载本地 Embedding 模型（首次运行会下载模型，约100MB）...")
    # 使用国内镜像下载模型，速度飞快
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    
    print("3. 正在将分块写入 Chroma 向量库...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db", # 数据将保存在这个文件夹
        collection_name="campus_policy"
    )
    print(f"成功存入 {len(chunks)} 个分块到向量库！")
    return vectorstore

if __name__ == "__main__":
    build_vectorstore()