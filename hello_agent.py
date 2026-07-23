"""Day 1: Python basics for an AI application."""

name = input("请输入你的名字：").strip()
school = input("请输入你的学校：").strip()
study_minutes = int(input("请输入今天学习了多少分钟：").strip())
study_hours = study_minutes / 60
if study_minutes >= 60:
    print("学习状态：很好，今天保持住！")
elif study_minutes >= 30:
    print("学习状态：不错，明天可以再多学一点。")
else:
    print("学习状态：先从 30 分钟开始，持续比一次学很久更重要。")
if not name:
    name = "同学"

learning_goal = "构建企业知识库问答助手"

print(f"你好，{name}！")
print(f"你的学习目标是：{learning_goal}。")
print("今天你已经成功运行了第一个 AI 项目 Python 程序。")
print(f"我来自：{school}。")
