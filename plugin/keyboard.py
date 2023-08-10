import cv2 as cv
import pyautogui

pyautogui.PAUSE = 0
history_press = None
disabled = False
keys = ['Q', 'W', 'E', 'R', 'T', 'Y',
        'U', 'I', 'O', 'P', 'A', 'S',
        'D', 'F', 'G', 'H', 'J', 'K',
        'L', 'Z', 'X', 'C', 'V', 'B',
        'N', 'M', ',', '.', '?', '!']


def disable(d):
    global disabled
    disabled = d


def keyboard_print_rec(image):
    """
    Print keyboard on screen.
    :param image: cv image
    :return: new CV Image
    """
    if disabled:
        return image

    # 绘制键盘
    global history_press
    for y in range(100, 600, 100):
        index_y = (y-100)//100
        for x in range(200, 1100, 150):
            index_x = (x-200)//150
            if history_press and keys[index_y*6+index_x] == history_press:
                cv.rectangle(image, (x, y), (x + 80, y + 80), (255, 0, 0), 2)
                history_press = None
            else:
                cv.rectangle(image, (x, y), (x + 80, y + 80), (0, 255, 0), 2)
            cv.putText(image, keys[index_y*6+index_x], (x+40, y+40), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)

    return image


def keyboard_on_key(pos, i):
    """
    Check if finger is on a specified button.
    :param pos: Finger position.
    :param i: Button index.
    :return: Boolean, True if on key.
    """
    if disabled:
        return False

    x, y = pos
    ind_x, ind_y = (150*(i % 6)+200), (100*(i // 6)+100)
    return ind_x <= x <= ind_x+80 and ind_y <= y <= ind_y+80


def keyboard_loop(pos):
    """
    Check if finger is on a button.
    :param pos: Finger position.
    :return: Button index / None if not on button.
    """
    if disabled:
        return None

    global history_press
    for i in range(len(keys)):
        if keyboard_on_key(pos, i):
            history_press = keys[i]
            return keys[i]
    else:
        return None


def keyboard_press(x):
    """
    Press a key.
    :param x: key index
    :return: None
    """
    if disabled:
        return "DISABLED"

    pyautogui.press(keys[x])

