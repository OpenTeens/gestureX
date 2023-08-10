import cv2 as cv
import pyautogui

pyautogui.PAUSE = 0
stx, sty = 0, 100
key_siz = 60
rax, ray = 120, 80
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
    # 绘制键盘
    global history_press
    for y in range(sty, 5 * ray + sty, ray):
        index_y = (y - sty) // ray
        for x in range(stx, 6 * rax + stx, rax):
            index_x = (x - stx) // rax
            if history_press and keys[index_y * 6 + index_x] == history_press:
                cv.rectangle(image, (x, y), (x + key_siz, y + key_siz), (255, 0, 0), 2)
                history_press = None
            else:
                cv.rectangle(image, (x, y), (x + key_siz, y + key_siz), (0, 255, 0), 2)
            cv.putText(image, keys[index_y * 6 + index_x], (x + (key_siz // 2), y + (key_siz // 2)),
                       cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)

    return image


def keyboard_on_key(pos, i, size):
    x, y = pos
    ind_x, ind_y = (rax * (i % 6) + stx), (ray * (i // 6) + sty)
    return ind_x <= x <= ind_x + size and ind_y <= y <= ind_y + size


def keyboard_loop(pos):
    global history_press
    for i in range(len(keys)):
        if keyboard_on_key(pos, i, key_siz):
            history_press = keys[i]
            return keys[i]
    else:
        return None


def keyborad_press(x):
    pyautogui.press(keys[x])
