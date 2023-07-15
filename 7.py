import simpleguitk as simplegui
import math
import random

# 定义全局变量
WIDTH = 800             # 画布宽度
HEIGHT = 600            # 画布高度
score = 0               # 游戏得分
fallings = 100          # 坠物个数
lives = 3               # 游戏机会次数（财神的命）
wealthgod = None        # 财神对象
falling_group = set()   # 所有坠物对象的集合

# 定义图片信息类
class ImageInfo:
    def __init__(self, center, size, radius=0, number=0, animated=False, count=None):
        self.center = center                # 图片的中心坐标
        self.size = size                    # 图片的大小
        self.radius = radius                # 图片的半径，用来计算是否和其它对象发生碰撞
        self.number = number                # 图片的编号，用于判断是哪一种坠物
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

    def get_animated(self):
        return self.animated

# 定义财神类
class Wealthgod:
    def __init__(self, pos, vel, acc, image, info):
        self.pos = pos                         # 财神的位置坐标
        self.vel = vel                         # 财神的水平速度
        self.acc = acc                         # 财神的水平加速度
        self.image = imagex                     # 财神图像对象
        self.image_center = info.get_center()  # 图片的中心坐标
        self.image_size = info.get_size()      # 图片的大小
        self.radius = info.get_radius()        # 图片的半径，用来计算是否和其它对象发生碰撞
        self.current_frame = 0

    def get_position(self):
        # 步骤1 请在此处补充代码
        return self.pos


    def get_radius(self):
        # 步骤1 请在此处补充代码
        return self.get_radius

    # 改变位置、速度
    def update(self):
        # 步骤1 请在此处补充代码，以实现财神在有加速度和摩擦减速的情况下，在游戏窗口下方移动
        self.pos[0] = (self.pos[0]+ self.vel) % WIDTH
        self.vel += self.acc
        self.vel *= 1 - 0.05

    # 显示财神
    def draw(self, canvas):
        # 步骤1 请在此处补充代码，以实现财神的动画显示
        self.update()
        self.current_frame += 1
        image_center = [wealthgod_info.center[0] + self.current_frame // 20 % wealthgod_info.count *
                        wealthgod_info.size[0],wealthgod_info.center[1]]
        canvas.draw_image(self.image, image_center, self.image_size,self.pos,self.image_size,0)

# 定义坠落物类
class Falling:
    def __init__(self, pos, image, info, sound=None):
        self.pos = pos
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.number = info.get_number()
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

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center , self.image_size, self.pos, self.image_size, 0)

    def update(self):        
        # 步骤2 请在此处补充代码
        self.pos[1] += 1
        if self.pos[1] < HEIGHT:
            return True
        else:
            return False

# 加载图片资源
start_info = ImageInfo([400, 300], [800, 600])
start_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@start.png")                    # 开始背景

background_info = ImageInfo([195, 110], [391, 220])
background_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@background.jpg")          # 游戏背景

wealthgod_info = ImageInfo([56.66, 72.5], [113.33, 145], 20, 0, True, 3)
wealthgod_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@wealthgod.png")            # 财神，图像文件中包含3副图片用来实现动画

diamond_info = ImageInfo([25, 25], [50, 50],20, 1)
diamond_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@diamond.png")                # 钻石

ingot_info = ImageInfo([25, 25], [50, 50],20, 2)
ingot_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@ingot.png")                    # 元宝

copper_info = ImageInfo([25, 25], [50, 50],20, 3)
copper_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@copper.png")                  # 铜钱

dog_info = ImageInfo([25, 25], [50, 50],20, 4)
dog_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@dog.png")                        # 恶狗

bomb_info = ImageInfo([25, 25], [50, 50],20, 5)
bomb_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@bomb.png")                      # 炸弹

startButton_info = ImageInfo([114, 50], [228, 99])
startButton_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@startbutton.png")       # 游戏开始按钮

end_info = ImageInfo([400, 300], [800, 600])
end_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@end.png")                        # 游戏结束按钮

collision_info = ImageInfo([55, 43], [110, 86])
collision_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@bomb.png")           # 炸弹爆炸效果

blood_info = ImageInfo([85.5, 85.5], [171, 171])
blood_image = simplegui.load_image("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@blood.png")                   # 被恶狗咬后的溅血效果

# 加载音效资源
back_sound = simplegui.load_sound("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@sound1.OGG")                    # 背景音效
explode_sound = simplegui.load_sound("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@explode.wav")                # 爆炸音效
money_sound = simplegui.load_sound("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@money.wav")                    # 捡到元宝或钱的音效
dog_sound = simplegui.load_sound("http://mooc.xjau.edu.cn:80/asset-v1:XJAU_CS+CS001+2019_T1+type@asset+block@dog.wav")                        # 被恶狗咬的音效

# 游戏开始函数
def game_start():
    # 设置游戏状态、得分、游戏机会次数、播放背景音乐，并在屏幕底部中间位置出现财神
    global wealthgod
    timer.start()
    back_sound.rewind()
    back_sound.play()
    wealthgod = Wealthgod([WIDTH/2, HEIGHT - wealthgod_info.get_size()[0]/2], 0, 0, wealthgod_image, wealthgod_info)

# 天空坠物随机出现函数，用来产生天空坠物的时间处理函数
def falling_spawner():
    # 步骤3 请在此处补充代码，以实现利用随机函数产生天空坠物的id，钻石、元宝、铜钱、恶狗、炸弹对应id依次为1,2,3,4,5
    global falling_group,falling_id, fallings
    if fallings > 0:
        x = random.randrange(25,WIDTH - 25)
        falling_id = random.randint(1,6)
        if falling_id == 1:
            a_falling = Falling([x,diamond_info.get_center()[1]], diamond_image,diamond_info)
        elif falling_id == 2:
            a_falling = Falling([x, ingot_info.get_center()[1]], ingot_image,ingot_info)
        elif falling_id == 3:
            a_falling = Falling([x,copper_info.get_center()[1]],copper_image,copper_info)

        elif falling_id == 4:
            a_falling = Falling([x,bomb_info.get_center()[1]], dog_image,dog_info)

        else:
            a_falling = Falling([x,bomb_info.get_center()[1]],bomb_image,bomb_info)
        falling_group.add(a_falling)
        fallings -= 1
    else:
        timer.stop()


# 处理一组坠物的辅助函数
def process_falling_group(group, canvas):
    # 步骤4 请在此处补充代码
    tmp_set = set([])
    for a_falling in list(group):
        a_falling.draw(canvas)
        if not a_falling.update():
            tmp_set.add(a_falling)
    group.difference_update(tmp_set)


# 主绘制函数
def draw(canvas):
    global wealthgod, falling_group
    canvas.draw_image(background_image, background_info.get_center(), background_info.get_size(),
                      [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_text('坠物剩余：' + str(fallings), (100, 30), 16, 'White', 'serif')
    canvas.draw_text('成绩：' + str(score), (WIDTH/2, 30), 16, 'White', 'serif')
    canvas.draw_text('生命数：' + str(lives), (WIDTH - 200, 30), 16, 'White', 'serif')
    wealthgod.draw(canvas)
    process_falling_group(falling_group, canvas)
    # 步骤5 已实现（不需要添加代码）

# 处理键盘按下事件的函数    
def key_down(key):
    global wealthgod
    # 步骤6 请在此处补充代码，以实现财神水平加速度的更新
    if key == simplegui.KEY_MAP["left"]:
        wealthgod.acc -= 0.1
    elif key == simplegui.KEY_MAP["right"]:
        wealthgod.acc += 0.1

# 处理键盘按下事件的函数
def key_up(key):
    global wealthgod
    # 步骤6 请在此处补充代码,，以实现财神水平加速度停止更新，变化为0
    wealthgod.acc = 0

# 创建用户界面
frame = simplegui.create_frame("欢天喜地接元宝", WIDTH, HEIGHT)

# 注册事件处理函数
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

# 创建定时器,2秒掉一个坠物
timer = simplegui.create_timer(2000, falling_spawner)

# 启动游戏
game_start()
frame.start()