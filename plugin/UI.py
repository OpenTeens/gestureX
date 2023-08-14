import cv2 as cv
import tkinter

Keyboard_status = "Off"
Keyboard_color = (0, 0, 255)
Mouse_status = "Off"
Mouse_color = (0, 0, 255)
Blackboard_status = "Off"
Blackboard_color = (0, 0, 255)


def calc_right_bond(left_bond, text):
    text_width = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.7, 5)[0][0]
    return left_bond + text_width + 40  # 40 for padding.


def new_button(image, x, name, status, color):
    right_bond = calc_right_bond(x, name)

    cv.rectangle(image, (x, 10), (right_bond, 40), (255, 255, 255), -1)
    cv.putText(image, status, (x + 50, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    cv.putText(image, status, (x + 50, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv.LINE_AA)
    cv.rectangle(image, (x, 40), (right_bond, 90), (0, 0, 0), 2)
    cv.rectangle(image, (x, 10), (right_bond, 40), (0, 0, 0), 2)
    cv.putText(image, name, (x + 20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    cv.putText(image, name, (x + 20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)


def buttons(debug_image):
    new_button(debug_image, 200, "Mouse", Mouse_status, Mouse_color)
    new_button(debug_image, 400, "Keyboard", Keyboard_status, Keyboard_color)
    new_button(debug_image, 600, "Blackboard", Blackboard_status, Blackboard_color)

    # Blackboard #######################################################
    # cv.rectangle(debug_image, (900, 10), (1050, 40), (255, 255, 255), -1)
    # cv.putText(debug_image, Blackboard_status, (950, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    # cv.putText(debug_image, Blackboard_status, (950, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, Blackboard_color, 2, cv.LINE_AA)
    # cv.rectangle(debug_image, (900, 40), (1050, 90), (0, 0, 0), 2)
    # cv.rectangle(debug_image, (900, 10), (1050, 40), (0, 0, 0), 2)
    # cv.putText(debug_image, "Blackboard", (920, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    # cv.putText(debug_image, "Blackboard", (920, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)

    # Keyboard #######################################################
    # cv.rectangle(debug_image, (700, 10), (850, 40), (255, 255, 255), -1)
    # cv.putText(debug_image, Keyboard_status, (750, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    # cv.putText(debug_image, Keyboard_status, (750, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, Keyboard_color, 2, cv.LINE_AA)
    # cv.rectangle(debug_image, (700, 40), (850, 90), (0, 0, 0), 2)
    # cv.rectangle(debug_image, (700, 10), (850, 40), (0, 0, 0), 2)
    # cv.putText(debug_image, "Keyboard", (720, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    # cv.putText(debug_image, "Keyboard", (720, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)
    #
    # # Mouse #######################################################
    # cv.rectangle(debug_image, (500, 10), (650, 40), (255, 255, 255), -1)
    # cv.putText(debug_image, Mouse_status, (550, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    # cv.putText(debug_image, Mouse_status, (550, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, Mouse_color, 2, cv.LINE_AA)
    # cv.rectangle(debug_image, (500, 10), (650, 40), (0, 0, 0), 2)
    # cv.rectangle(debug_image, (500, 40), (650, 90), (0, 0, 0), 2)
    # cv.putText(debug_image, "Mouse", (520, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    # cv.putText(debug_image, "Mouse", (520, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)


def check_on_buttons(pos, debug_image):
    global Keyboard_status, Keyboard_color, Mouse_color, Mouse_status, Blackboard_color, Blackboard_status
    x, y = pos

    if y <= 40 or y >= 90:
        return x, False, False

    if 200 < x < calc_right_bond(200, "Mouse"):
        Mouse_status, Mouse_color = reverse_status(Mouse_status, Mouse_color)
        button_name = 'mouse'
        status = (Mouse_status == 'On')
        cv.rectangle(debug_image, (200,40), (calc_right_bond(200, "Mouse"), 90), (255,0,0), -1)
    elif 400 < x < calc_right_bond(400, "Keyboard"):
        Keyboard_status, Keyboard_color = reverse_status(Keyboard_status, Keyboard_color)
        button_name = 'keyboard'
        status = (Keyboard_status == 'On')
        cv.rectangle(debug_image, (400,40), (calc_right_bond(400, "Keyboard"), 90), (255,0,0), -1)
    elif 600 < x < calc_right_bond(600, "Blackboard"):
        Blackboard_status, Blackboard_color = reverse_status(Blackboard_status, Blackboard_color)
        button_name = 'blackboard'
        status = (Blackboard_status == 'On')
        cv.rectangle(debug_image, (600,40), (calc_right_bond(600, "Blackboard"), 90), (255,0,0), -1)
    else:
        return x, False, False

    return button_name, True, status


def reverse_status(status, color):
    if status == 'Off':
        status = 'On'
        color = (0, 255, 0)
    else:
        status = 'Off'
        color = (0, 0, 255)

    return status, color
