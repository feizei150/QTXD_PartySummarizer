# 🧠 AI党建文档总结自动化系统（v1.0）

一个用于自动化总结党建文档的智能系统，支持批量读取 `.docx` 文件，自动区分“草稿撰写类”与“资料总结类”，调用本地大模型生成标准格式总结文本，输出为 `.txt` 文件，适合用于支部材料梳理、年度汇报、学习教育成果提炼等场景。

---

## ✨ 功能特性

- 自动识别党建文稿类型（草稿 / 总结）
- 支持 Word `.docx` 文件自动读取，无需转换格式
- 使用本地大模型（支持 deepseek / mistral / llama3 等）
- 自动输出 `_总结.txt` 到指定文件夹
- 内置党建文稿提示词模板（四要素结构）
- 全本地运行，保障数据安全，适配单位/政府场景

---

## 🛠 使用说明

### 📁 项目结构

```
QTXD_party_summarizer/
├─ party_documents/         # 放入 .docx 文件
├─ party_summaries/         # 自动输出总结结果
├─ summarize_party_docs.py  # 主脚本
└─ requirements.txt         # 安装依赖
```

### 📦 安装依赖

```bash
pip install -r requirements.txt
```

### 🚀 执行脚本

```bash
python summarize_party_docs.py
```

运行后，所有 `.docx` 文件将自动被读取、分类、总结，输出到 `party_summaries` 文件夹。

---

## 🔧 模型支持

系统支持以下模型选项：

- `deepseek-r1:7b` - 总结能力强，适合正式文稿（需8G以上内存）
- `llama3:8b` - 中文总结准确，条理清晰
- `mistral:7b` - 占用资源低，适合轻量草稿场景

> 默认模型在脚本第 5 行修改：
> ```python
> MODEL = "mistral:latest"
> ```

---

## 📚 使用示例

系统已在党支部实际运行，适用于：

- 党建学习计划总结
- 八项规定精神教育归纳
- 支部年度汇报草稿草拟
- 党员教育问题清单提炼

---

## 🧩 后续规划

- 接入 Notion/Obsidian 笔记系统
- 自动发送总结邮件
- 网页端上传总结（Flask/Python GUI）
- 提供网页版/小程序版本

---

## 👨‍💼 作者

由“擎天AI项目组”自主研发，欢迎私聊合作。

📬 联系方式请见说明书或 GitHub 页面。
