"""Day 2: Search relevant paragraphs in an enterprise policy file."""

from pathlib import Path


policy_path = Path("company_policy.txt")
policy_text = policy_path.read_text(encoding="utf-8")

keyword = input("请输入要查询的关键词（例如：报销、请假、密码）：").strip()

if not keyword:
    print("你没有输入关键词，程序结束。")
else:
    paragraphs = policy_text.split("\n\n")
    matched_paragraphs = [paragraph for paragraph in paragraphs if keyword in paragraph]

    if matched_paragraphs:
        print(f"\n找到 {len(matched_paragraphs)} 条相关制度：\n")
        for index, paragraph in enumerate(matched_paragraphs, start=1):
            print(f"--- 结果 {index} ---")
            print(paragraph)
    else:
        print(f"没有找到包含“{keyword}”的制度内容。")
