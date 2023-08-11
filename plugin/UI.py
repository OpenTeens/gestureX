import cv2 as cv

Keyboard_status = "Off"
Keyboard_color = (0, 0, 255)
Mouse_status = "Off"
Mouse_color = (0, 0, 255)
Blackboard_status = "Off"
Blackboard_color = (0, 0, 255)


def buttons(debug_image):
    # Blackboard #######################################################
    cv.rectangle(debug_image, (900, 10), (1050, 40), (255, 255, 255), -1)
    cv.putText(debug_image, Blackboard_status, (950, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    cv.putText(debug_image, Blackboard_status, (950, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, Blackboard_color, 2, cv.LINE_AA)
    cv.rectangle(debug_image, (900, 40), (1050, 90), (0, 0, 0), 2)
    cv.rectangle(debug_image, (900, 10), (1050, 40), (0, 0, 0), 2)
    cv.putText(debug_image, "Blackboard", (920, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    cv.putText(debug_image, "Blackboard", (920, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)

    # Keyboard #######################################################
    cv.rectangle(debug_image, (700, 10), (850, 40), (255, 255, 255), -1)
    cv.putText(debug_image, Keyboard_status, (750, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    cv.putText(debug_image, Keyboard_status, (750, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, Keyboard_color, 2, cv.LINE_AA)
    cv.rectangle(debug_image, (700, 40), (850, 90), (0, 0, 0), 2)
    cv.rectangle(debug_image, (700, 10), (850, 40), (0, 0, 0), 2)
    cv.putText(debug_image, "Keyboard", (720, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    cv.putText(debug_image, "Keyboard", (720, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)

    # Mouse #######################################################
    cv.rectangle(debug_image, (500, 10), (650, 40), (255, 255, 255), -1)
    cv.putText(debug_image, Mouse_status, (550, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    cv.putText(debug_image, Mouse_status, (550, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, Mouse_color, 2, cv.LINE_AA)
    cv.rectangle(debug_image, (500, 10), (650, 40), (0, 0, 0), 2)
    cv.rectangle(debug_image, (500, 40), (650, 90), (0, 0, 0), 2)
    cv.putText(debug_image, "Mouse", (520, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5, cv.LINE_AA)
    cv.putText(debug_image, "Mouse", (520, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)


def check_on_buttons(pos):
    global Keyboard_status, Keyboard_color, Mouse_color, Mouse_status, Blackboard_color, Blackboard_status
    x, y = pos

    if y <= 40 or y >= 90:
        return x, False, False

    if 500 < x < 650:
        Mouse_status, Mouse_color = reverse_status(Mouse_status, Mouse_color)
        button_name = 'mouse'
        status = True if Mouse_status == 'On' else False
    elif 700 < x < 850:
        Keyboard_status, Keyboard_color = reverse_status(Keyboard_status, Keyboard_color)
        button_name = 'keyboard'
        status = True if Keyboard_status == 'On' else False
    elif 900 < x < 1050:
        Blackboard_status, Blackboard_color = reverse_status(Blackboard_status, Blackboard_color)
        button_name = 'blackboard'
        status = True if Blackboard_status == 'On' else False
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
