

---
license: apache-2.0
sdk: streamlit
app_file: app.py
---

# 🎓 校园政策问答助手 (RAG + Agent)

基于 RAG（检索增强生成）的智能问答系统，支持南大、复旦、西电等高校政策文件。
集成 Agent 工具调用：支持政策问答、计算 GPA、查询课表。

## 🚀 在线体验
（部署成功后填入链接）

## 🛠️ 技术栈
- 文档分块：固定长度 vs 标题层级（对比实验）
- 向量库：Chroma（本地持久化）
- 检索模型：BAAI/bge-small-zh-v1.5（本地推理）
- 大模型：智谱 GLM-4-Flash（免费 API）
- 前端：Streamlit