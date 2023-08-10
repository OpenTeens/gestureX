import cv2 as cv
import pyautogui

pyautogui.PAUSE = 0
stx, sty = 0, 100
key_siz = 60
rax, ray = 120, 80
history_press = None
disabled = False
sizeX = 8
sizeY = 5

keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'Q', 'W', 'E', 'R', 'T', 'Y',
        'U', 'I', 'O', 'P', 'A', 'S',
        'D', 'F', 'G', 'H', 'J', 'K',
        'L', 'Z', 'X', 'C', 'V', 'B',
        'N', 'M', ',', '.', '?', '!']


def disable(d):
    global disabled
    disabled = d


def keyboard_print_rec(image):
    if disabled:
        return "DISABLED"

    # 绘制键盘
    global history_press

    for y in range(sty, sizeY * ray + sty, ray):
        index_y = (y - sty) // ray
        for x in range(stx, sizeX * rax + stx, rax):
            index_x = (x - stx) // rax
            if history_press and keys[index_y * sizeX + index_x] == history_press:
                cv.rectangle(image, (x, y), (x + key_siz, y + key_siz), (255, 0, 0), 2)
                history_press = None
            else:
                cv.rectangle(image, (x, y), (x + key_siz, y + key_siz), (0, 255, 0), 2)
            cv.putText(image, keys[index_y * sizeX + index_x], (x + (key_siz // 2), y + (key_siz // 2)),
                       cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)


def keyboard_on_key(pos, i, size):
    if disabled:
        return False

    x, y = pos
    ind_x, ind_y = (rax * (i % sizeX) + stx), (ray * (i // sizeX) + sty)
    return ind_x <= x <= ind_x + size and ind_y <= y <= ind_y + size


def keyboard_loop(pos):
    if disabled:
        return None

    global history_press
    for i in range(len(keys)):
        if keyboard_on_key(pos, i, key_siz):
            history_press = keys[i]
            return keys[i]
    else:
        return None


def keyborad_press(x):
    if disabled:
        return "DISABLED"

    pyautogui.press(keys[x])
