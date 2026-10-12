import os
os.environ["HF_HUB_DISABLE_SSL_VERIFY"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"  # 强制离线运行，以后永远不会再报这个红字
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. 加载环境变量（包含你在 .env 里配置的 ZHIPU_API_KEY）
load_dotenv()

def get_rag_chain():
    # 2. 加载本地 Embedding 模型（必须和建库时用的一致）
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    
    # 3. 加载 Chroma 向量库
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings,
        collection_name="campus_policy"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4}) # 检索最相关的4个块

    # 4. 初始化 LLM（使用智谱 API，兼容 OpenAI 格式）
    llm = ChatOpenAI(
        model="glm-4-flash", # 免费模型
        api_key=os.getenv("ZHIPU_API_KEY"),
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        temperature=0.1
    )

    # 5. 定义提示词模板（约束它不要瞎编）
    prompt = ChatPromptTemplate.from_template("""你是一个校园政策问答助手。请严格根据以下参考文档回答用户问题。
如果文档中没有相关信息，请直接回答“根据现有资料无法确认，建议咨询教务处”，不要自己编造。

参考文档：
{context}

用户问题：{question}

回答要求：
1. 引用具体条款编号
2. 如果涉及条件判断，列出所有条件
3. 回答末尾标注信息来源""")

    # 6. 构建 RAG 链
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, retriever

if __name__ == "__main__":
    print("正在初始化 RAG 系统...")
    chain, retriever = get_rag_chain()
    
    # 测试问题
    test_question = "学士学位的授予条件是什么？"
    print(f"\n用户提问：{test_question}")
    
    print("\n--- 正在检索相关文档 ---")
    docs = retriever.invoke(test_question)
    for i, doc in enumerate(docs):
        print(f"[{i+1}] {doc.page_content[:100]}...")
        
    print("\n--- 正在生成回答 ---")
    answer = chain.invoke(test_question)
    print(f"\nAI回答：\n{answer}")