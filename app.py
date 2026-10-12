import streamlit as st
from src.agent_chain import get_agent

st.set_page_config(page_title="校园政策问答助手", page_icon="🎓", layout="centered")
st.title("🎓 校园政策问答助手 (Agent 版)")
st.markdown("支持：政策问答 | 计算 GPA | 查询课表")

@st.cache_resource
def load_agent():
    return get_agent()

with st.spinner("正在加载 Agent 工具链..."):
    agent = load_agent()

question = st.text_input("💬 请输入你的问题（如：学士学位的授予条件是什么？/ 帮我算 GPA / 查课表）")

if question:
    with st.spinner("Agent 正在思考并调用工具..."):
        # 适配 LangChain 1.0 新 API
        result = agent.invoke({"messages": [("user", question)]})
        answer = result["messages"][-1].content
    st.markdown("### 🤖 回答")
    st.success(answer)