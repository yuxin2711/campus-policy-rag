import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import Tool
from src.rag_chain import get_rag_chain
from src.tools import calculate_gpa, query_course_schedule

load_dotenv()

def get_agent():
    rag_chain, retriever = get_rag_chain()
    
    rag_tool = Tool(
        name="campus_policy_rag",
        func=lambda q: rag_chain.invoke(q),
        description="用于回答关于校园政策、学生手册、学籍、奖学金、学位授予等规章制度的问题。输入应该是完整的用户问题。"
    )
    
    tools = [rag_tool, calculate_gpa, query_course_schedule]
    
    llm = ChatOpenAI(
        model="glm-4-flash",
        api_key=os.getenv("ZHIPU_API_KEY","11b33f5c78544af598ab1d2b857cba66.ctM4TNALonc4CvMW"),
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        temperature=0.1
    )
    
    # LangChain 1.0 新写法，自动处理工具调用循环
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="你是一个校园助手，可以回答政策问题、计算GPA、查询课表。请根据用户问题选择合适的工具。"
    )
    
    return agent

if __name__ == "__main__":
    agent = get_agent()
    
    print("--- 测试 1：政策问题 ---")
    result = agent.invoke({"messages": [("user", "学士学位的授予条件是什么？")]})
    print(result["messages"][-1].content)
    
    print("\n--- 测试 2：计算 GPA ---")
    result = agent.invoke({"messages": [("user", "帮我算一下我的GPA，高数:85,英语:90,物理:78")]})
    print(result["messages"][-1].content)
    
    print("\n--- 测试 3：查课表 ---")
    result = agent.invoke({"messages": [("user", "帮我查一下学号2023001在2025-2026-1学期的课表")]})
    print(result["messages"][-1].content)