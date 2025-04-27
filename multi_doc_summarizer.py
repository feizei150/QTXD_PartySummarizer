import os
from flask import Flask, request, render_template_string, send_file
from werkzeug.utils import secure_filename
from ollama import Client
from docx import Document

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
MODEL = "deepseek-r1:7b"
client = Client(host="http://localhost:11434")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>多文档智能总结器</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-10">
  <div class="max-w-3xl mx-auto bg-white p-6 shadow rounded">
    <h1 class="text-2xl font-bold mb-4">📥 上传多个文件进行总结分析</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="files" multiple accept=".docx,.txt" class="mb-4">
      <button type="submit" class="bg-indigo-600 text-white px-4 py-2 rounded">上传并总结</button>
    </form>
    {% if summary %}
    <div class="mt-6">
      <h2 class="text-xl font-semibold">🧠 智能总结结果：</h2>
      <pre class="bg-gray-100 p-4 mt-2 whitespace-pre-wrap">{{ summary }}</pre>
    </div>
    {% endif %}
  </div>
</body>
</html>
'''

def extract_text(filepath):
    if filepath.endswith(".docx"):
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])
    elif filepath.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

@app.route("/", methods=["GET", "POST"])
def upload():
    summary = None
    if request.method == "POST":
        uploaded_files = request.files.getlist("files")
        all_text = ""
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            all_text += extract_text(save_path) + "\n"

        # 调用 Ollama 模型生成总结
        response = client.chat(model=MODEL, messages=[{
            "role": "user",
            "content": f'''请你作为党建文稿专家，根据以下多份文件内容，生成结构清晰、语言规范、符合党建风格的总结材料。

要求：
1. 概括核心精神要点（不少于3点）
2. 提炼任务方向或阶段计划
3. 总结可参考内容，提炼出对个人或支部的可行动建议
4. 如发现不清晰/待改进之处，也请列出并提出建议

请输出完整公文风总结：\n{all_text}'''
        }])
        summary = response["message"]["content"]

        output_path = os.path.join(OUTPUT_FOLDER, "总结结果.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

    return render_template_string(HTML_TEMPLATE, summary=summary)

if __name__ == "__main__":
    app.run(debug=True, port=7860)
