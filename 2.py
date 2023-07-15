import math
import simpleguitk
import random

# 初始化全局变量
random_num = 0
num_range = 10
remain_time = 0

def new_game():
    global random_num, num_range, remain_time
    remain_time = int(math.ceil(math.log(num_range + 1, 2)))
    print("\n欢迎来到购物街！")
    print("新一轮商品竞猜开始。竞猜价格范围从0到", num_range)
    print("总的竞猜机会有", remain_time,"次")
    random_num = random.randrange(0, num_range)

def range10():
    global num_range
    num_range = 10
    new_game()

def range100():
    global num_range
    num_range = 100
    new_game()

def range1000():
    global num_range
    num_range = 1000
    new_game()

def input_guess(guess):
    global random_num, remain_time
    guess = int(guess)
    remain_time -= 1
    print("你猜的价格是:", guess)
    if remain_time > 0:
        if guess == random_num:
            print("竞猜正确！")
            new_game()
        elif guess > random_num:
            print("比实际价格高了")
        else:
            print("比实际价格低了")
        print("剩余竞猜次数:", remain_time)
    else:
        print("竞猜次数已用完，商品实际价格是:", random_num)
        new_game()

new_game()

frame = simpleguitk.create_frame('猜物价游戏', 300, 300)

frame.add_button('价格范围: 0-10', range10, 200)
frame.add_button('价格范围: 0-100', range100, 200)
frame.add_button('价格范围: 0-1000', range1000, 200)
frame.add_input('输入你的竞猜价格:', input_guess, 200)

frame.start()