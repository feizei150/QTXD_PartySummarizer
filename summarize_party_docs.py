import os
from ollama import Client
from docx import Document

MODEL = "deepseek-r1:7b"
INPUT_DIR = r"E:\QTXD_AI_system\QTXD_party_summarizer\party_documents"
OUTPUT_DIR = r"E:\QTXD_AI_system\QTXD_party_summarizer\party_summaries"

client = Client()
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 加载 .docx 内容
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

# 判断是计划草稿，还是学习总结
def get_prompt_type(filename: str):
    filename = filename.lower()
    if any(keyword in filename for keyword in ["计划", "问题", "自学", "清单", "安排"]):
        return "draft"
    else:
        return "summary"

# 获取对应提示词
def build_prompt(text, mode):
    if mode == "draft":
        return [
            {"role": "system", "content": "请根据以下内容，补全或优化这份党建工作文稿的初稿。尽量保持原意、语言严谨，适合作为党建学习计划、问题清单、工作安排等文档。"},
            {"role": "user", "content": text}
        ]
    else:
        return [
            {"role": "system", "content": "你是党建专家，请将下列内容按党建汇报标准进行总结，包括：1）简要背景；2）重点工作亮点；3）存在问题；4）下一步改进建议。总结结果请分条列出，尽量简洁清晰。"},
            {"role": "user", "content": text}
        ]

# 主处理流程
for file_name in os.listdir(INPUT_DIR):
    if file_name.endswith(".docx"):
        file_path = os.path.join(INPUT_DIR, file_name)
        text = extract_text_from_docx(file_path)
        mode = get_prompt_type(file_name)

        print(f"📄 正在处理：{file_name} → 模式：{'草稿优化' if mode == 'draft' else '内容总结'}")
        response = client.chat(
            model=MODEL,
            messages=build_prompt(text, mode)
        )

        summary = response['message']['content']
        output_name = file_name.replace(".docx", "_总结.txt")
        output_path = os.path.join(OUTPUT_DIR, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"✅ 总结完成：{output_name}")
