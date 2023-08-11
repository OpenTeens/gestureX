import pyautogui
import threading
import cv2 as cv

SENSITIVITY = 1  # 触控板敏感度

TB_START = (100, 100)
TB_END = (860, 440)
TB_WIDTH = TB_END[0] - TB_START[0]
TB_HEIGHT = TB_END[1] - TB_START[1]

disabled = False
last = [0, 0]
pyautogui.FAILSAFE = False


# 上次鼠标坐标

def disable(d):
    global disabled
    disabled = d


def move_to(tp):
    """
    :param tp: 摄像头点位置
    :return: 无
    """
    if disabled:
        return "DISABLED"

    def helper():
        x, y = tp
        x, y = x - TB_START[0], y - TB_START[1]
        screen_width, screen_height = pyautogui.size()

        # 自稳定系统
        global last
        if (x - last[0]) ** 2 + (y - last[1]) ** 2 <= 10 ** 2:
            return

        last = [x, y]

        # 读取屏幕尺寸
        ratio_x, ratio_y = screen_width / TB_WIDTH, screen_height / TB_HEIGHT
        ratio_x *= SENSITIVITY
        ratio_y *= SENSITIVITY

        # 变换摄像头坐标到屏幕坐标
        screen_x, screen_y = x * ratio_x, y * ratio_y
        if 0 <= screen_x <= screen_width and 0 <= screen_y <= screen_height:
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
    """
    Release mouse.
    :return: None
    """
    if disabled:
        return "DISABLED"

    pyautogui.mouseUp()


def print_touchboard(image):
    """
    Print touchboard rectangle on screen.
    :param image: cv image
    :return: None
    """
    if disabled:
        return "DISABLED"

    cv.rectangle(image, TB_START, TB_END, (0, 255, 0), 2)
