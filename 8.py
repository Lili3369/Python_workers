import simpleguitk as simplegui
import math
import random

# 定义全局变量
WIDTH = 800             # 画布宽度
HEIGHT = 600            # 画布高度
score = 0               # 游戏得分
time = 120              # 游戏限定时间（剩余时间  秒）
lives = 3               # 游戏机会次数（财神的命）
started = False         # 游戏是否开始
over = False            # 游戏状态（是否结束）
wealthgod = None        # 财神对象
falling_group = set([])  # 所有天空坠物对象的集合
offset = 0               # 用于财神图片的微量平移，从而实现财神的动画效果

# 定义图片信息类
class ImageInfo:
    def __init__(self, center, size, radius=0, number=0,
                 lifespan=None, animated=False, count=None):
        self.center = center                # 图片的中心坐标
        self.size = size                    # 图片的大小
        self.radius = radius                # 图片的半径，用来计算是否和其它对象发生碰撞
        self.number = number                # 图片的编号，用于判断是哪一种坠物
        if lifespan:
            self.lifespan = lifespan        # 由该图片生成对象的寿命，以帧为单位，通常每秒为60帧
        else:
            self.lifespan = float('inf')    # 表示无穷大
        self.animated = animated            # 由该图片生成对象是否具备动画效果
        self.count = count                  # 为实现动画效果所提供的平铺图片数量

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_number(self):
        return self.number

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# 定义财神类
class Wealthgod:
    def __init__(self, pos, vel, acc, image, info):
        self.pos = [pos[0], pos[1]]            # 财神的位置坐标
        self.vel = vel                         # 财神的水平速度
        self.acc = acc                         # 财神的水平加速度
        self.image = image                     # 财神图像对象
        self.image_center = info.get_center()  # 图片的中心坐标
        self.image_size = info.get_size()      # 图片的大小
        self.radius = info.get_radius()        # 图片的半径，用来计算是否与其它对象发生碰撞

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    # 改变位置、速度
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel) % WIDTH
        self.vel += self.acc
        self.vel *= 0.99

    # 显示财神
    def draw(self, canvas):
        self.update()
        image_center = [wealthgod_info.center[0] + (offset * 10 // 10) % wealthgod_info.count * wealthgod_info.size[0],
                        wealthgod_info.center[1]]
        canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, 0)

# 定义坠落物类
class Falling:
    def __init__(self, pos, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.number = info.get_number()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_position(self):
        return self.pos    

    def get_radius(self):
        return self.radius

    def get_number(self):
        return self.number

    # 坠物碰撞到财神
    def collide(self, other_object):
        # 请在此处补充代码
        if dist(self.get_position(),
                other_object.get_position()) <= self.radius + other_object.get_radius():
            return True
        else:
            return False

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center , self.image_size,
                          self.pos, self.image_size, 0)

    def update(self):        
        self.pos[1] = (self.pos[1] + 1) % HEIGHT
        self.age += 1
        if self.age < self.lifespan:
            return True
        else:
            return False

# 加载图片资源
start_info = ImageInfo([400, 300], [800, 600])
start_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@start.png")                 # 开始背景

background_info = ImageInfo([195, 110], [391, 220])
background_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@background.jpg")       # 游戏背景

wealthgod_info = ImageInfo([56.66, 72.5], [113.33, 145], 0, 0, None, True, 3)
wealthgod_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@wealthgod.png")         # 财神，图像文件中包含3副图片用来实现动画

diamond_info = ImageInfo([25, 25], [50, 50],20, 1)
diamond_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@diamond.png")             # 钻石

ingot_info = ImageInfo([25, 25], [50, 50],20, 2)
ingot_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@ingot.png")                 # 元宝

copper_info = ImageInfo([25, 25], [50, 50],20, 3)
copper_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@copper.png")               # 铜钱

dog_info = ImageInfo([25, 25], [50, 50],20, 4)
dog_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@dog.png")                     # 恶狗

bomb_info = ImageInfo([25, 25], [50, 50],20, 5)
bomb_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@bomb.png")                   # 炸弹

startButton_info = ImageInfo([114, 50], [228, 99])
startButton_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@startbutton.png")    # 游戏开始按钮

end_info = ImageInfo([400, 300], [800, 600])
end_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@end.png")                     # 游戏结束按钮

collision_info = ImageInfo([55, 43], [110, 86])
collision_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@collision.png")        # 炸弹爆炸效果

blood_info = ImageInfo([85.5, 85.5], [171, 171])
blood_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@blood.png")                # 被恶狗咬后的溅血效果

# 加载音效资源
back_sound = simplegui.load_sound("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@sound1.OGG")                 # 背景音效
explode_sound = simplegui.load_sound("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@explode.wav")             # 爆炸音效
money_sound = simplegui.load_sound("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@money.wav")                 # 捡到元宝或钱的音效
dog_sound = simplegui.load_sound("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@dog.wav")                     # 被恶狗咬的音效

# 定义距离函数
def dist(p, q):
    # 请在此处补充代码
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)#距离

# 游戏初始化辅助函数
# 同时也是“再来一局”按钮事件处理函数
def init():
    # 设置游戏状态、得分、游戏限定时间、游戏机会次数，禁用背景音乐
    global offset, started, over, score, lives, time
    offset = 0          # 用于财神图片的微量平移，从而实现财神的动画效果
    # 请在此处补充代码
    started = False
    over = False
    score = 0
    lives = 3
    time = 120
    back_sound.pause

# 游戏开始函数
def game_start():
    # 设置游戏状态、得分、游戏机会次数、播放背景音乐，并在屏幕底部中间位置出现财神
    global started, over, score, lives, wealthgod
    started = True
    over = False
    timer.start()
    back_sound.rewind()
    back_sound.play()
    wealthgod = Wealthgod([WIDTH / 2,
                           HEIGHT - wealthgod_info.get_size()[0]/2],
                          0, 0,
                          wealthgod_image,
                          wealthgod_info)

# 游戏结束函数
def game_over():
    # 设置游戏状态、得分、游戏机会次数
    global started, over, time
    started = False
    over = True
    time = 0

# 计时器事件处理函数：用于随机出现天空坠物
def falling_spawner():
    # 利用随机函数产生天空坠物的id，钻石、元宝、铜钱、恶狗、炸弹对应id依次为1,2,3,4,5
    global falling_group, time, falling_number
    if started:
        x = random.randrange(25, WIDTH - 25)
        falling_number = random.randint(1, 5)
        if falling_number == 1:
            a_falling = Falling([x, diamond_info.get_center()[1]], diamond_image, diamond_info)
        elif falling_number == 2:
            a_falling = Falling([x, ingot_info.get_center()[1]], ingot_image, ingot_info)
        elif falling_number == 3:
            a_falling = Falling([x, copper_info.get_center()[1]], copper_image, copper_info)
        elif falling_number == 4:
            a_falling = Falling([x, dog_info.get_center()[1]], dog_image, dog_info)
        elif falling_number == 5:
            a_falling = Falling([x, bomb_info.get_center()[1]], bomb_image, bomb_info)
        falling_group.add(a_falling)
        time -= 1  

# 检测一组对象（天空坠物）和一个对象（财神）之间是否发生碰撞的辅助函数
def group_collide(group, other_object, canvas):
    # 坠物与财神碰撞时，全局变量发生变化
    global score, lives, wealthgod, over, started
    # 请在此处补充代码
    tmp_set = set([])
    collided = False
    for a_falling in list(group):
        if a_falling.collide(other_object):
            tmp_set.add(a_falling)
            collided = True
            if lives == 0:
                over = True
                started = False
            else:
                if a_falling.get_number()==1:
                    score += 10
                elif a_falling.get_number()==2:
                    score += 5
                elif a_falling.get_number() ==3:
                    score += 1
                elif a_falling.get_number() ==4:
                    score -=5
                elif a_falling.get_number() ==5:
                    score -= 10
                    lives -= 1
                    wealthgod = Wealthgod([WIDTH / 2, HEIGHT - wealthgod_info.get_size()[0]/2],
                                          0,0,wealthgod_image,wealthgod_info)
        group.difference_update(tmp_set)
        return collided


# 在画布上画一组坠物的辅助函数
def process_falling_group(group, canvas):
    tmp_set = set([])
    for a_falling in list(group):
        a_falling.draw(canvas)
        if not over and not a_falling.update():
            tmp_set.add(a_falling)
    group.difference_update(tmp_set) 

# 绘图事件处理函数
def draw(canvas):
    global time, score, lives, over, started, wealthgod, falling_group, offset
    offset += 0.1        # 用于实现财神图片的微量偏移
    if not started and not over:
        canvas.draw_image(start_image,
                          start_info.get_center(),
                          start_info.get_size(), 
                          [WIDTH / 2, HEIGHT / 2],
                          [WIDTH, HEIGHT])
    elif over or time == 0:
        timer.stop()
        canvas.draw_image(end_image, 
                          end_info.get_center(), 
                          end_info.get_size(),
                          [WIDTH / 2, HEIGHT / 2],
                          end_info.get_size())
        canvas.draw_text('总成绩\n'+" "+ str(score), (20, HEIGHT-100),36, 'Red', 'serif')
        game_over()
    else:    
        canvas.draw_image(background_image, 
                          background_info.get_center(), 
                          background_info.get_size(),
                          [WIDTH / 2, HEIGHT / 2],
                          [WIDTH, HEIGHT])
        canvas.draw_text('时间：' + str(time), (100, 30), 16, 'White', 'serif')
        canvas.draw_text('成绩：' + str(score), (WIDTH/2, 30), 16, 'White', 'serif')
        canvas.draw_text('还有：' + str(lives) + "次机会", (WIDTH - 200, 30), 16, 'White', 'serif')

        wealthgod.draw(canvas)

        process_falling_group(falling_group, canvas)
        if group_collide(falling_group, wealthgod, canvas):
            if lives > 0:
                wealthgod.draw(canvas)
            else:
                over = True

# 鼠标点击事件处理函数
def mouse_click(pos):
    # 请在x此处补充代码，以实现鼠标单击“开始游戏”位置处，游戏开始
    global started
    if not started and not over:
        if 85 < pos[0] < 234 and 418 < pos[1] < 478:
            game_start()

# 键盘按下事件处理函数
def key_down(key):
    global wealthgod
    if key == simplegui.KEY_MAP["left"]:         # 向左
        wealthgod.acc -= 0.01
    elif key == simplegui.KEY_MAP["right"]:      # 向右
        wealthgod.acc += 0.01

# 处理键盘按下事件的函数
def key_up(key):
    global wealthgod
    wealthgod.acc = 0

# 创建用户界面
frame = simplegui.create_frame("欢天喜地接元宝", WIDTH, HEIGHT)

# 请在此处补充代码，以实现绘制“再来一局”按钮
frame.add_button("再来一局",init,50)

# 注册事件处理函数
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_click)

# 创建定时器，2秒掉一个坠物
timer = simplegui.create_timer(2000, falling_spawner)

# 启动游戏
init()
frame.start()