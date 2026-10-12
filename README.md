---
sdk: streamlit
app_file: app.py
---

# 🎓 校园政策问答助手 (RAG + Agent)

> 🎥 **在线演示视频**：[点击在 B站 查看完整功能演示](https://www.bilibili.com/video/BV13QpR6iE1K/?vd_source=f969351d5f21ddbf60dfc3ee98934077)

基于 RAG（检索增强生成）与 Agent 工具调用的校园政策问答助手。支持：政策问答 | GPA计算 | 课表查询。

## 🚀 本地一键运行
1. `git clone https://github.com/yuxin2711/campus-policy-rag.git`
2. `pip install -r requirements.txt`
3. 在根目录新建 `.env`，写入 `ZHIPU_API_KEY=你的密钥`
4. `streamlit run app.py`
5. 打开浏览器访问 `http://localhost:8501`