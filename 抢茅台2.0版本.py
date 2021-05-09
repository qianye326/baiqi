from pymouse import PyMouse
import win32con
import win32api
import time,requests
start = time.time()
m = PyMouse()
#方案一
def paly1():
    m = PyMouse()
    print(m.position())
    m.click(76, 812, 1, 1)

def paly2():
    # 第一步鼠标放置地方点击两下
    m = PyMouse()
    move = m.position()
    x = move[0]
    y = move[1]
    m.click(x, y, 1, 1)
    # 第二步吧鼠标移动到购物车处等待0.3秒
    m.move(138, 816)
    time.sleep(0.5)
    # 第三步点击结算按钮
    m.click(488, 379, 1, 2)
    time.sleep(0.8)
    # 第四步进去结算界面获取结算表点，并点击等待0.3
    m.click(463, 605, 1, 2)
    # 第五步滚动页面点击提交按钮
    time.sleep(1.6)
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1000)
    m.click(442, 580, 1, 2)
    print(m.position())
    end = time.time()
    print(end - start)

def paly3():

    m = PyMouse()
    move = m.position()
    x = move[0]
    y = move[1]
    m.click(x, y, 1, 1)
    #如果直接跳到购车
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1000)
    time.sleep(0.8)
    m.click(513, 401, 1, 1)
    end = time.time()
    print(end - start)

while True:
    t = time.ctime()
    if '20:00:00' in t:
        paly3()
    else:
        pass
# print(m.position())
# win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1000)