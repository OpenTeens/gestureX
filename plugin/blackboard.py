import cv2 as cv
import numpy as np
import cv2 as cv

# CONSTANTS
GRID_SIZE = 20  # px
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GRID_WIDTH = (SCREEN_WIDTH // GRID_SIZE) + 1
GRID_HEIGHT = (SCREEN_HEIGHT // GRID_SIZE) + 1

# GLOBAL VARIABLES
disabled = False
history = []
history_paras = []
grid = [[[] for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
pen_color = (0, 225, 0)
thickness = 3


def disable(d):
    global disabled
    disabled = d


def pen(new):
    """
    Add new pen path to `history`.
    :param new: new pen pos
    :return: None
    """
    if disabled:
        return "DISABLED"

    new = new.copy()
    history.append(new)
    history_paras.append([pen_color])
    if new[0] is not None:
        grid_add(new)


def none(_):
    return None


def grid_add(new):
    """
    Add new point to `grid`.
    :param new: new pen pos
    :return: None
    """
    x, y = new

    if x is None or x > SCREEN_WIDTH or y > SCREEN_HEIGHT:
        return

    g = grid[x // GRID_SIZE][y // GRID_SIZE]
    g.append(new)


def distance(p1, p2):
    """
    Calculate distance (squared) between two points.
    :param p1: point 1
    :param p2: point 2
    :return: squared distance
    """
    if p1[0] is None or p2[0] is None:
        return 0
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def draw_color(color):
    """
    Convert color name to BGR.
    :param color: color name
    :return: BGR color
    """
    if disabled:
        return "DISABLED"

    # blue, green red
    if color == "Purple":
        return (255, 0, 255)
    elif color == "Blue":
        return (255, 0, 0)
    elif color == "Green":
        return (0, 255, 0)
    elif color == "Red":
        return (0, 0, 255)
    elif color == "Yellow":
        return (0, 255, 255)
    elif color == "Pink":
        return (203, 192, 255)
    elif color == "Eraser":
        return (0, 0, 0)


def draw_button(image, y, color):
    """
    Draw a button on screen.
    :param image: cv image
    :param y: y coord
    :param color: color in BGR
    :return: None
    """
    if disabled:
        return "DISABLED"

    color_of_button = draw_color(color)
    right_bound = 170
    cv.putText(image, color, (70, y + 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, color_of_button, 2, cv.LINE_AA)
    cv.rectangle(image, (50, y), (right_bound, y + 50), (0, 0, 0), 2)


def draw_all_buttons(image):
    """
    Draw all buttons on screen.
    :param image: cv image
    :return: None
    """
    if disabled:
        return "DISABLED"

    draw_button(image, 150, "Purple")
    draw_button(image, 200, "Blue")
    draw_button(image, 250, "Green")
    draw_button(image, 300, "Red")
    draw_button(image, 350, "Yellow")
    draw_button(image, 400, "Pink")
    draw_button(image, 450, "Eraser")


def inRect(x, y, left_top, right_bottom):
    """
    Check if a point is in a rectangle.
    :param x: pos x
    :param y: pos y
    :param left_top: box left-top point
    :param right_bottom: box right-bottom point
    :return: whether (x, y) is in rect
    """
    if disabled:
        return None

    if left_top[0] <= x <= right_bottom[0] and left_top[1] <= y <= right_bottom[1]:
        return True

    return False


def choose_color(debug_image, pos):
    """
    Choose pen color.
    :param pos: finger pos
    :return: Activated Mode Function
    """
    if disabled:
        return None

    global pen_color
    x, y = pos

    # blue, green red
    if inRect(x, y, (50, 150), (170, 150 + 50)):
        pen_color = (255, 0, 255)
    elif inRect(x, y, (50, 200), (170, 200 + 50)):
        pen_color = (255, 0, 0)
    elif inRect(x, y, (50, 250), (170, 250 + 50)):
        pen_color = (0, 255, 0)
    elif inRect(x, y, (50, 300), (170, 300 + 50)):
        pen_color = (0, 0, 255)
    elif inRect(x, y, (50, 350), (170, 350 + 50)):
        pen_color = (0, 255, 255)
    elif inRect(x, y, (50, 400), (170, 400 + 50)):
        pen_color = (203, 192, 255)
    elif inRect(x, y, (50, 450), (170, 450 + 50)):
        return erase
    else:
        return None
    return pen


def changeThickness(key):
    if disabled:
        return "DISABLED"
    global thickness
    thickness = int(chr(key))


def print_history(image):
    """
    Print pen trace on screen.
    :param image: cv image
    :return: None
    """

    if disabled:
        return "DISABLED"

    last_h = None
    for i in range(len(history)):
        h = history[i]
        paras = history_paras[i]
        if h[0] is None:
            # normalize
            if last_h is None:
                del h
                del paras
                continue
            else:
                last_h = None

            # 稳定系统
            if i + 1 < len(history) and distance(history[i - 1], history[i + 1]) < 5 ** 2:
                del h
                del paras

            continue
        if last_h is not None:
            # change the color of the open
            cv.line(image, tuple(last_h), tuple(h), paras[0], thickness)
        last_h = h


def erase(pos, radius=15):
    """
    Erase all pen traces which in a circle.
    :param pos: central pos
    :param radius: eraser radius
    :return: None
    """
    if disabled:
        return "DISABLED"

    x, y = pos
    if x >= SCREEN_WIDTH or y >= SCREEN_HEIGHT:
        return

    x, y = pos
    eraser_grids = set()
    for bound_x in [x + radius, x - radius, x]:
        for bound_y in [y + radius, y - radius, y]:
            eraser_grids.add((bound_x // GRID_SIZE, bound_y // GRID_SIZE))

    for g in eraser_grids:  # grid
        for p in grid[g[0]][g[1]]:  # point
            if (p[0] - x) ** 2 + (p[1] - y) ** 2 <= radius ** 2:
                p[0] = None
                p[1] = None
                grid[g[0]][g[1]].remove(p)


def clear():
    if disabled:
        return "DISABLED"

    global history, grid, history_paras
    history = []
    history_paras = []
    grid = [[[] for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]


def export(mode=0):
    """
    Export pen trace to image.
    :param mode: 0: last trace, 1: all traces
    :return: png image
    """
    if disabled:
        return "DISABLED"

    exp_history = []
    exp_history_paras = []
    if mode == 0:
        # generate last trace
        pen_start_index = 0
        for i in range(len(history) - 1, -1, -1):
            if history[i][0] is None:
                pen_start_index = i + 1
                break
        exp_history = history[pen_start_index:]
        exp_history_paras = history_paras[pen_start_index:]
    elif mode == 1:
        # generate all traces
        exp_history = history.copy()
        exp_history_paras = history_paras.copy()

    if len(exp_history) == 0:
        # No pen trace.
        return None

    # Find the bounding box of pen trace.
    p1 = [SCREEN_WIDTH, SCREEN_HEIGHT]
    p2 = [0, 0]
    for h in exp_history:
        if h[0] is None:
            continue

        p1[0] = min(p1[0], h[0])
        p1[1] = min(p1[1], h[1])
        p2[0] = max(p2[0], h[0])
        p2[1] = max(p2[1], h[1])

    # Calculate image size.
    p1[0] = max(0, p1[0] - 20)
    p1[1] = max(0, p1[1] - 20)
    p2[0] = min(SCREEN_WIDTH, p2[0] + 20)
    p2[1] = min(SCREEN_HEIGHT, p2[1] + 20)

    img_width = p2[0] - p1[0]
    img_height = p2[1] - p1[1]
    delta = (img_width - img_height) // 2
    if mode == 0:
        if img_width > img_height:
            p1 = [p1[0], p1[1] - delta]
        else:
            p1 = [p1[0] - delta, p1[1]]
        img_width = img_height = max(img_width, img_height)

    # Draw pen trace on image.
    image = 255 * np.ones(shape=[img_height, img_width, 3], dtype=np.uint8)  # blank image with white background
    last_h = None
    for i in range(len(exp_history)):
        h = exp_history[i]
        paras = exp_history_paras[i]

        if h[0] is None:
            last_h = None
            continue

        h = (h[0] - p1[0], h[1] - p1[1])  # add bias

        if last_h is None:
            last_h = h
            continue

        cv.line(image, last_h, h, paras[0], 3)  # draw line (black)
        last_h = h
        # cv: blue, green, red
    return image, p1


def save(mode=0):
    """
    Save image to file.
    :return: None
    """
    if disabled:
        return "DISABLED"

    cv.imwrite("output.png", export(mode)[0])
