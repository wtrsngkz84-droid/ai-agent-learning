"""Day 2: Search relevant paragraphs in an enterprise policy file."""

from pathlib import Path


policy_path = Path("company_policy.txt")
policy_text = policy_path.read_text(encoding="utf-8")

paragraphs = policy_text.split("\n\n")

print("企业制度查询助手已启动。输入“退出”结束程序。")

while True:
    keyword = input("\n请输入要查询的关键词（例如：报销、请假、密码）：").strip()

    if keyword in {"退出", "exit", "q"}:
        print("查询助手已结束，欢迎下次使用。")
        break

    if not keyword:
        print("你没有输入关键词，请重新输入。")
        continue

    matched_paragraphs = [paragraph for paragraph in paragraphs if keyword in paragraph]

    if matched_paragraphs:
        print(f"\n找到 {len(matched_paragraphs)} 条相关制度：\n")
        for index, paragraph in enumerate(matched_paragraphs, start=1):
            print(f"--- 结果 {index} ---")
            print(paragraph)
    else:
        print(f"没有找到包含“{keyword}”的制度内容。")
