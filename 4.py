import simpleguitk as simplegui
import random

# 初始化全局变量
WIDTH = 500  # 画布宽度
HEIGHT = 500  # 画布高度

PADDLE_WIDTH = 50  # 挡板宽度
PADDLE_HEIGHT = 8  # 挡板高度
paddle_pos = WIDTH / 2  # 挡板初始位置
paddle_vel = 0  # 挡板初始速度
HALF_PADDLE_WIDTH = PADDLE_WIDTH / 2
HALF_PADDLE_HEIGHT = PADDLE_HEIGHT / 2

BALL_RADIUS = 8  # 壁球半径
ball_pos = [WIDTH / 2, HEIGHT / 2]  # 壁球初始位置
ball_vel = [0, 0]  # 壁球初始速度

# 发球
def spawn_ball():
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.random() + 1, random.random() + 1]

def new_game():
    global score, live, paddle_pos, paddle_vel
    score = 0
    live = 3
    paddle_pos = WIDTH / 2
    paddle_vel = 0
    spawn_ball()

def draw(canvas):
    global score, live, paddle_pos, ball_pos, ball_vel

    #画线
    canvas.draw_line([0,250],[500,250],5,"white")
    canvas.draw_line([250,250],[250,500],5,"white")

    # 绘制小球
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "Yellow", "Yellow")

    # 绘制挡板
    canvas.draw_polygon([(paddle_pos - HALF_PADDLE_WIDTH, HEIGHT - PADDLE_HEIGHT),
                         (paddle_pos + HALF_PADDLE_WIDTH, HEIGHT - PADDLE_HEIGHT),
                         (paddle_pos + HALF_PADDLE_WIDTH, HEIGHT),
                         (paddle_pos - HALF_PADDLE_WIDTH, HEIGHT)],
                        1, "White", "White")

    # 绘制生命和分数
    canvas.draw_text("Lives: " + str(live), (10, 30), 20, "White")
    canvas.draw_text("分数: " + str(score), (WIDTH - 150, 30), 20, "White")

    # 更新小球位置
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    #检查与上壁碰撞
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # 检查与左右壁的碰撞
    if ball_pos[0] <= BALL_RADIUS or ball_pos[0] >= WIDTH - BALL_RADIUS:
        ball_vel[0] = -ball_vel[0]

    # 更新挡板的水平位置
    if (paddle_pos + paddle_vel >= HALF_PADDLE_WIDTH) and (paddle_pos + paddle_vel <= WIDTH - HALF_PADDLE_WIDTH):
        paddle_pos += paddle_vel

    # 检查与挡板的碰撞
    if ball_pos[1] >= HEIGHT - BALL_RADIUS - PADDLE_HEIGHT and (paddle_pos - HALF_PADDLE_WIDTH <= ball_pos[0] <= paddle_pos + HALF_PADDLE_WIDTH):
        ball_vel[1] = -ball_vel[1] * 1.1
        ball_vel[0] *= 1.1
        score += 1
        if score >= 50:
            canvas.draw_text("You win!", (WIDTH/2 - 50, HEIGHT/2), 30, "White")
            ball_vel[0] = 0
            ball_vel[1] = 0
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS- PADDLE_HEIGHT:
        live -= 1
        if live > 0:
            spawn_ball()
        else:
            if score < 50:
                canvas.draw_text("Game over.", (WIDTH/2 - 60, HEIGHT/2), 30, "White")
            ball_vel[0] = 0
            ball_vel[1] = 0
            live = 0

def keydown(key):
    global paddle_vel
    if key == simplegui.KEY_MAP['left']:
        paddle_vel = -4  # 改变速度方向
    elif key == simplegui.KEY_MAP['right']:
        paddle_vel = 4

def keyup(key):
    global paddle_vel
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        paddle_vel = 0

# 创建框架
frame = simplegui.create_frame("单人壁球", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_canvas_background("Black")
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("重新开始", new_game, 50)

# 运行框架
new_game()
frame.start()