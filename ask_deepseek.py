"""Day 3: Make the first DeepSeek API call."""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(Path(__file__).with_name(".env"))
api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()

if not api_key:
    raise SystemExit(
        "没有找到 DEEPSEEK_API_KEY。请复制 .env.example 为 .env，并填入你的 API Key。"
    )

if not api_key.isascii() or "你的" in api_key:
    raise SystemExit(
        "DEEPSEEK_API_KEY 仍是示例文字或包含中文。请在 .env 中替换为真实的 sk-... 密钥。"
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

question = input("你想问 DeepSeek 什么？\n> ").strip()

if not question:
    raise SystemExit("问题不能为空。")

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {
            "role": "system",
            "content": "你是一个耐心的 Python 学习助手，请用简洁、易懂的中文回答。",
        },
        {"role": "user", "content": question},
    ],
)

print("\nDeepSeek：")
print(response.choices[0].message.content)
