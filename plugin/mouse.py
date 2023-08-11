import pyautogui
import threading

disabled = False
last = [0, 0]


# 上次鼠标坐标

def disable(d):
    global disabled
    disabled = d


def move_to(tp: tuple, photo_width=960, photo_height=540):
    """
    :param tp: 摄像头点位置
    :param photo_width: 摄像头宽
    :param photo_height: 摄像头高
    :return: 无
    """
    if disabled:
        return "DISABLED"

    def helper():
        x, y = tp
        screen_width, screen_height = pyautogui.size()

        # 自稳定系统
        global last
        if (x - last[0]) ** 2 + (y - last[1]) ** 2 <= 10 ** 2:
            return

        last = [x, y]
        # 读取屏幕尺寸
        ratio_x, ratio_y = screen_width / photo_width, screen_height / photo_height
        # 变换摄像头坐标到屏幕坐标
        screen_x, screen_y = x * ratio_x, y * ratio_y
        pyautogui.moveTo(screen_x, screen_y)

    pyautogui.PAUSE = 0
    threading.Thread(target=helper).run()
    # 多线程提升效率


def mouse_press():
    """
    :return: 点击（具体调用逻辑待定）
    """

    if disabled:
        return "DISABLED"
    pyautogui.mouseDown() 

def mouse_up():
    pyautogui.mouseUp()
