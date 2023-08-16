import cv2 as cv
import tkinter

statuses = ["Off", "Off", "Off", "Off"]
btn_names = ["Mouse", "Keyboard", "Blackboard", "StableDiff"]


def calc_right_bond(left_bond, text):
    text_width = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.7, 5)[0][0]
    return left_bond + text_width + 40  # 40 for padding.


def new_button(image, x, name, i):
    status = statuses[i]
    color = getColor(status)
    right_bond = calc_right_bond(x, name)

    cv.rectangle(image, (x, 10), (right_bond, 40), (255, 255, 255), -1)
    cv.putText(image, status, (x + 30, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    cv.putText(image, status, (x + 30, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv.LINE_AA)
    cv.rectangle(image, (x, 40), (right_bond, 90), (0, 0, 0), 2)
    cv.rectangle(image, (x, 10), (right_bond, 40), (0, 0, 0), 2)
    cv.putText(image, name, (x + 20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    cv.putText(image, name, (x + 20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)


def getColor(status):
    if status == 'On':
        return (0, 255, 0)
    else:
        return (0, 0, 255)


def buttons(debug_image):
    for i in range(len(statuses)):
        new_button(debug_image, 200 + i * 200, btn_names[i], i)


def check_on_buttons(pos, debug_image):
    x, y = pos

    if y <= 40 or y >= 90:
        return x, False, False

    for i in range(len(statuses)):
        start = 200 + i * 200
        end = calc_right_bond(start, btn_names[i])
        if start < x < end:
            reverse_status(i)
            cv.rectangle(debug_image, (start, 40), (end, 90), (255, 0, 0), -1)
            return btn_names[i].lower(), True, (statuses[i] == 'On')

    return x, False, False


def reverse_status(i):
    if statuses[i] == "Off":
        statuses[i] = "On"
    else:
        statuses[i] = "Off"
