# Day 3：大模型调用环境准备

## 目标

学会使用独立虚拟环境，并理解为什么 API Key 必须放在 `.env`，不能直接写进 Python 文件或上传到 GitHub。

## 创建虚拟环境

在 VS Code 终端运行：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

如果终端前出现 `(.venv)`，说明虚拟环境已激活。

## 配置 DeepSeek

1. 在 DeepSeek 开放平台创建 API Key。
2. 复制 `.env.example`，并将副本命名为 `.env`。
3. 在 `.env` 中填入你的真实 API Key：

```text
DEEPSEEK_API_KEY=你的真实密钥
```

不要把真实密钥发给任何人，也不要提交 `.env`。

## 运行第一次调用

```powershell
python ask_deepseek.py
```

可以输入：`请用一句话解释什么是 RAG？`
