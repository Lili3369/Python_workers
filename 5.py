import simpleguitk as simplegui
import random
import math

# 画布的尺寸
WIDTH = 480
HEIGHT = 150

# 牌的尺寸
CARD_WIDTH = 60
CARD_HEIGHT = 100

cards = []             # 保存4对牌的列表
flipped_cards = []     # 记录翻过的牌
steps = 0

# 初始化一组字母牌
def init_cards():
    global cards
    all_characters= ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    cards.clear()
    random.shuffle(all_characters)
    for i in range(4):
        one_card = all_characters.pop();
        # 注意：cards中的元素也是列表。该列表的第一个元素是某个字母，
        # 第二个元素表示该牌是否被翻过来，0表示没翻过来，1表示翻过来。
        cards.append([one_card, 0])  
        cards.append([one_card, 0])
    random.shuffle(cards)

def new_game():
    global steps
    flipped_cards.clear()
    steps = 0
    init_cards()


def draw(canvas):
    # 代码写在这里 
    pass
    # 步骤1：绘制牌
    for i, card in enumerate(cards):
        point_list = [(i*CARD_WIDTH,0),((i+1)*CARD_WIDTH,0),
                      ((i+1)*CARD_WIDTH,CARD_HEIGHT),(i*CARD_WIDTH,CARD_HEIGHT)]
        char_position = [(i + 0.25) * CARD_WIDTH,CARD_HEIGHT* 0.8]
        if card[1] ==0:
            canvas.draw_polygon(point_list,2, "black","green")
        else:
            canvas.draw_polygon(point_list,2,"black","white")
            canvas.draw_text(card[0],char_position, CARD_HEIGHT*0.4,"black","Times New Rome")

    # 步骤3： 显示步数
    canvas.draw_text("步数： "+ str(steps),[0,HEIGHT],12,"white")



def mouse_click(pos):
    global steps, cards, flipped_cards
    # 步骤2： 实现游戏主要步骤
    card_index = math.floor(pos[0]/CARD_WIDTH)
    if cards[card_index][1] == 0:
        flipped_cards.append(card_index)
        cards[card_index][1] = 1
        steps += 1
        if len(flipped_cards) > 2:
            if cards[flipped_cards[0]][0] != cards[flipped_cards[1]][0]:
                     cards[flipped_cards[0]][1] = 0
                     cards[flipped_cards[1]][1] = 0

            flipped_cards.pop(0)
            flipped_cards.pop(0)



# 创建用户界面
frame = simplegui.create_frame("超级大脑", WIDTH, HEIGHT)
frame.set_canvas_background("Black")
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_click)

# 创建按钮
frame.add_button("开始游戏", new_game, 80)

new_game()
frame.start()