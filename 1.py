"""
石头剪刀布游戏
该程序的关键点是把“石头”、“剪刀”、“布”映射为以下数字：
石头 - 0
剪刀 - 1
布 - 2
"""

import random   # 包含random.randrange(start, stop)函数的模块

# 定义辅助函数
def name_to_number(name):
    # 用if/elif/else将name转换为对应数字代码，-1表示name无效
    if name == "石头":
        return 0
    elif name == "剪刀":
        return 1
    elif name == "布":
        return 2
    else:
        return -1          # 无效的name返回-1


def number_to_name(number):
    # 用if/elif/else将数字代码number转换为对应的字符名称，number无效时返回"无效"
    if number ==0:
        return "石头"
    elif number ==1:
        return "剪刀"
    elif number ==2:
        return "布"
    else:
        return "无效"



# 程序从此执行
while True:
    print("石头剪刀布游戏开始！")
    print("输入'石头'、'剪刀'或'布'，输入'结束'游戏结束。")
    cmd = input("请出拳: ")#输出语句
    if cmd == '结束':
        print("游戏结束。")
        break

    player_number = name_to_number(cmd)
    if player_number == -1:
        print("出拳无效，游戏重新开始。")
        print("--------------------------------------\n")
        continue

    print("你出的拳是：" + cmd)
    computer_number = random.randrange(0, 3)  # 电脑随机出拳
    print("电脑出的拳是：" + number_to_name(computer_number))

    # 计算player_number和computer_number之差对3的模
    diff_mod_three = (player_number - computer_number) % 3

    # 用if/elif/else判定输赢结果，并输出结果信息
    if diff_mod_three == 0:
        print("你和电脑平手！")
        print("--------------------------------------\n")
    elif diff_mod_three == 1:
        print("电脑获胜！")
        print("--------------------------------------\n")
    else:
        print("你获胜！")
        print("--------------------------------------\n")