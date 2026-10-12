import re
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 加载文档函数
def load_documents(raw_dir: str):
    """读取 data/raw 下的所有 PDF 和 Word 文档"""
    docs = []
    raw_path = Path(raw_dir)
    
    for file in raw_path.glob("*.pdf"):
        print(f"正在加载 PDF: {file.name}")
        loader = PyPDFLoader(str(file))
        docs.extend(loader.load())
        
    for file in raw_path.glob("*.docx"):
        print(f"正在加载 Word: {file.name}")
        loader = Docx2txtLoader(str(file))
        docs.extend(loader.load())
        
    return docs

# 2. 策略 A：固定长度分块（基线）
def fixed_chunk(docs, chunk_size=500, overlap=50):
    """按固定字符数切分，允许重叠"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", "。", " ", ""]
    )
    return splitter.split_documents(docs)

# 3. 策略 B：按标题层级切分（结构感知）
def heading_chunk(docs, max_chunk_size=800):
    """按「第X章」「第X条」等结构切分，保留段落完整性"""
    chunks = []
    for doc in docs:
        text = doc.page_content
        # 用正则匹配「第X章」「第X条」「一、」「（一）」等常见标题
        pattern = r"(第[一二三四五六七八九十百\d]+[章条]|[一二三四五六七八九十]+、|（[一二三四五六七八九十]+）)"
        # 在标题前插入特殊标记，然后按标记切分
        formatted_text = re.sub(pattern, r"\n\n\1", text)
        sections = formatted_text.split("\n\n")
        
        current_chunk = ""
        for section in sections:
            if not section.strip():
                continue
            # 如果当前块加上新段落不超过最大限制，就合并
            if len(current_chunk) + len(section) <= max_chunk_size:
                current_chunk += section + "\n"
            else:
                # 超过限制，保存当前块，开始新块
                if current_chunk.strip():
                    new_doc = doc.model_copy()
                    new_doc.page_content = current_chunk.strip()
                    chunks.append(new_doc)
                current_chunk = section + "\n"
                
        # 保存最后一个块
        if current_chunk.strip():
            new_doc = doc.model_copy()
            new_doc.page_content = current_chunk.strip()
            chunks.append(new_doc)
            
    return chunks

if __name__ == "__main__":
    # 测试代码：读取文档并打印分块结果
    raw_dir = "data/raw"
    docs = load_documents(raw_dir)
    print(f"共加载了 {len(docs)} 页原始文档。\n")
    
    fixed_chunks = fixed_chunk(docs)
    heading_chunks = heading_chunk(docs)
    
    print(f"策略 A（固定长度）分块数：{len(fixed_chunks)}")
    print(f"策略 B（标题层级）分块数：{len(heading_chunks)}")
    
    print("\n--- 策略 B 的第一个 chunk 示例 ---")
    if heading_chunks:
        print(heading_chunks[0].page_content[:300] + "...\n")