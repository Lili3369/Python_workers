import simpleguitk as simplegui  

# 全局变量
message1 = "00:00.0"
message2 = "0/0"
counter = 0
success_times = 0
click_times = 0

# 辅助函数
def format():
    # 利用字符串的连接制式输出
    global message1, message2, success_times, click_times
    minute = str(counter // 600)
    second = str((counter // 10) % 60)
    tenth_second = str(counter % 10)
    if len(minute) == 1:
        minute = "0" + minute
    if len(second) == 1:
        second = "0" + second
    message1 = minute + ":" + second + "." + tenth_second
    message2 = str(success_times) + "/" + str(click_times)

def start():
    # 计时器开始计时
    if not timer.is_running():
        timer.start()


def pause():
    # 计时器停止，根据最后一位数字改变点击次数和成功次数，最后按格式输出
    global success_times, click_times, message1, counter
    timer.stop()
    click_times += 1
    if counter % 10 == 0:
        success_times += 1
    format()

def reset():
    # 计时器停止，全局变量初始化
    global counter, message1, message2, success_times, click_times 
    timer.stop()
    counter = 0
    success_times = 0
    click_times = 0
    format()

# 定义间隔0.1秒定时器事件函数
def tick():
    # 每隔0.1秒增加1
    global counter
    counter += 1
    format()   


# 定义绘制画布函数
def draw(canvas):
    global message1, message2 
    canvas.draw_text(message1, [250, 200], 50, "White")
    canvas.draw_text(message2, [450, 50], 30, "Green")

# 创建框架
frame = simplegui.create_frame("秒表", 600, 400)

# 创建计时器，每100毫秒(0.1秒)触发一次       
timer = simplegui.create_timer(100, tick)                 

# 创建按钮
frame.add_button("开始", start, 150)                      # 框架上增加”秒表开始“按钮        
frame.add_button("暂停", pause, 150)                      # 框架上增加”暂停“按钮
frame.add_button("复位", reset, 150)                      # 框架上增加”复位“按钮
frame.set_draw_handler(draw)                             # 执行画布绘制

# 框架开始执行
frame.start()