import simpleguitk as simplegui
import random

# 载入外部图像
baymax = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@baymax.jpg")

# 定义常量
# 画布的尺寸
WIDTH = 600
HEIGHT = WIDTH + 100

# 图像块的边长
IMAGE_SIZE = WIDTH / 3

# 图像块坐标列表
all_coordinates = [[IMAGE_SIZE*0.5, IMAGE_SIZE*0.5], [IMAGE_SIZE*1.5, IMAGE_SIZE*0.5],
                   [IMAGE_SIZE*2.5, IMAGE_SIZE*0.5], [IMAGE_SIZE*0.5, IMAGE_SIZE*1.5],
                   [IMAGE_SIZE*1.5, IMAGE_SIZE*1.5], [IMAGE_SIZE*2.5, IMAGE_SIZE*1.5],
                   [IMAGE_SIZE*0.5, IMAGE_SIZE*2.5], [IMAGE_SIZE*1.5, IMAGE_SIZE*2.5], None]

# 棋盘行列数
ROWS = 3
COLS = 3

# 移动步数
steps = 0

# 保存所有图像块的列表
board = [[None, None, None],
         [None, None, None],
         [None, None, None]]        

# 图像块类
class Square:
    def __init__(self, coordinate):
        self.center = coordinate

    def draw(self, canvas, board_pos):
        # 步骤1 代码写在这里
        canvas.draw_image(baymax,self.center,[IMAGE_SIZE,IMAGE_SIZE],
                          [(board_pos[1] + 0.5) * IMAGE_SIZE, (board_pos[0] + 0.5) *IMAGE_SIZE],
                          [IMAGE_SIZE,IMAGE_SIZE])

# 初始化拼图板
def init_board():
    # 打乱图像块坐标
    random.shuffle(all_coordinates)
    # 填充拼图板
    for i in range(ROWS):
        for j in range(COLS):
            idx = i * ROWS + j
            square_center = all_coordinates[idx]
            if square_center is None:
                board[i][j] = None
            else:
                board[i][j] = Square(square_center)

# 重置游戏    
def play_game():
    global steps
    steps = 0
    init_board()

# 绘制游戏界面各元素
def draw(canvas):
    # 画黑框
    canvas.draw_polygon([[0, 0], [WIDTH, 0], [WIDTH, WIDTH], [0, WIDTH]], 1, 'Black')

    # 画目标图像
    canvas.draw_image(baymax, [WIDTH/2, WIDTH/2], [WIDTH, WIDTH], [50, WIDTH+50], [98, 98])

    # 画步数
    canvas.draw_text("步数："+str(steps), [400, 680], 22, "White")

    # 画图像块
    # 步骤2 代码写在这里
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] is not None:
                board[i][j].draw(canvas,[i,j])



def mouseclick(pos):
    global steps
    # 将点击位置换算成拼图板上的坐标
    r = int(pos[1] // IMAGE_SIZE)
    c = int(pos[0] // IMAGE_SIZE)

    if r < 3 and c < 3:             # 点击位置在拼图板内才移动图片
        if board[r][c] is None:     # 点到空位置上什么也不移动
            return
        else:
            # 依次检查当前图像块的上,下,左,右是否有空位置，如果有就移动当前图像块
            # 步骤3 代码写在这里
            current_square  = board[r][c]
            if r- 1 >= 0 and board[r-1][c] is None:
                board[r][c] = None
                board[r - 1][c] = current_square
                steot += 1
            elif c+1<= 2 and board[r][c + 1] is None:
                board[r][c] = None
                board[r][c +1] = current_square
                steps +=1
            elif r + 1<= 2 and board[r +1][c] is None:
                board[r][c] = None
                board[r+1][c] = current_square
                steps += 1
            elif c - 1 >=0 and board[r][c-1] is None:
                board[r][c] = None
                board[r][c-1] = current_square
                steps += 1

# 创建框架
frame = simplegui.create_frame("拼图", WIDTH, HEIGHT)
frame.set_canvas_background("Black")
frame.set_draw_handler(draw)
frame.add_button("重新开始", play_game, 60)

# 注册鼠标事件
frame.set_mouseclick_handler(mouseclick)

# 初始化游戏
play_game()

# 启动框架
frame.start()