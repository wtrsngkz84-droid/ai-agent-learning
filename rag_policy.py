"""Minimal RAG assistant for enterprise policy questions."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_DIR = Path(__file__).parent
load_dotenv(PROJECT_DIR / ".env")

api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
if not api_key:
    raise SystemExit("没有找到 DEEPSEEK_API_KEY，请先检查并保存 .env 文件。")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

policy_text = (PROJECT_DIR / "company_policy.txt").read_text(encoding="utf-8")
paragraphs = policy_text.split("\n\n")

# 当前版本使用简单关键词检索；以后会升级成向量语义检索。
search_terms = {
    "考勤",
    "打卡",
    "迟到",
    "报销",
    "交通",
    "住宿",
    "发票",
    "费用",
    "请假",
    "申请",
    "密码",
    "客户资料",
    "源代码",
    "信息安全",
    "泄露",
}


def keyword_retrieve(question: str) -> list[str]:
    """Return policy paragraphs that share known terms with the question."""
    question_terms = [term for term in search_terms if term in question]
    scored_paragraphs = []

    for paragraph in paragraphs:
        score = sum(term in paragraph for term in question_terms)
        if score > 0:
            scored_paragraphs.append((score, paragraph))

    scored_paragraphs.sort(key=lambda item: item[0], reverse=True)
    return [paragraph for _, paragraph in scored_paragraphs[:2]]


def semantic_retrieve(question: str) -> list[str]:
    """Ask the LLM to select relevant paragraph IDs when keywords miss."""
    numbered_documents = "\n\n".join(
        f"[{index}] {paragraph}" for index, paragraph in enumerate(paragraphs)
    )

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是知识库检索器。根据用户问题选择直接相关的制度编号。"
                    "若没有任何制度能回答问题，必须返回空列表。"
                    '只输出 JSON，例如：{"relevant_ids": [0]} 或 '
                    '{"relevant_ids": []}。'
                ),
            },
            {
                "role": "user",
                "content": f"制度列表：\n{numbered_documents}\n\n用户问题：{question}",
            },
        ],
        response_format={"type": "json_object"},
        max_tokens=100,
    )

    try:
        result = json.loads(response.choices[0].message.content)
        relevant_ids = result.get("relevant_ids", [])
    except (json.JSONDecodeError, AttributeError):
        return []

    valid_ids = [
        document_id
        for document_id in relevant_ids
        if isinstance(document_id, int) and 0 <= document_id < len(paragraphs)
    ]
    return [paragraphs[document_id] for document_id in valid_ids[:2]]


question = input("请输入你的企业制度问题：\n> ").strip()
if not question:
    raise SystemExit("问题不能为空。")

retrieved_paragraphs = keyword_retrieve(question)
retrieval_method = "关键词检索"

if not retrieved_paragraphs:
    print("关键词没有命中，正在尝试语义检索……")
    retrieved_paragraphs = semantic_retrieve(question)
    retrieval_method = "DeepSeek 语义检索"

if not retrieved_paragraphs:
    raise SystemExit("知识库中没有相关制度，无法根据现有资料回答。")

context = "\n\n".join(retrieved_paragraphs)

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {
            "role": "system",
            "content": (
                "你是企业制度问答助手。只能根据用户提供的制度资料回答，"
                "不得编造；资料不足时必须明确说资料中没有说明。"
            ),
        },
        {
            "role": "user",
            "content": f"制度资料：\n{context}\n\n用户问题：{question}",
        },
    ],
)

print("\n助手回答：")
print(response.choices[0].message.content)
print(f"\n检索方式：{retrieval_method}")
print("\n引用制度：")
for paragraph in retrieved_paragraphs:
    title = paragraph.splitlines()[0]
    print(f"- {title}")
