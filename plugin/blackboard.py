import cv2 as cv
import numpy as np

# CONSTANTS
GRID_SIZE = 20  # px
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GRID_WIDTH = (SCREEN_WIDTH // GRID_SIZE) + 1
GRID_HEIGHT = (SCREEN_HEIGHT // GRID_SIZE) + 1

# GLOBAL VARIABLES
disabled = False
history = []
grid = [[[] for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]


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


def print_history(image):
    """
    Print pen trace on screen.
    :param image: cv image
    :return: None
    """
    if disabled:
        return "DISABLED"

    last_h = None
    for h in history:
        if h[0] is None:
            if last_h is None:  # normalize
                del h
            else:
                last_h = None
            continue
        if last_h is not None:
            cv.line(image, tuple(last_h), tuple(h), (0, 225, 0), 3)
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
    global history, grid
    history = []
    grid = [[[] for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

def blackboard_output():
    """
    Output pen trace to image file
    :return: None
    """

    #创建一个空白1280x720的图片
    img = np.full((720, 1280, 3), 255,dtype=np.uint8)
    print_history(img)
    cv.imwrite("output.png", img)

def export():
    """
    Export pen trace to image.
    :param mode: export mode, 0: all traces, 1: latest trace
    :param export_square: whether to export a square image
    :return: png image
    """
    if disabled:
        return "DISABLED"

    # generate last trace
    pen_start_index = 0
    for i in range(len(history) - 1, -1, -1):
        if history[i][0] is None:
            pen_start_index = i + 1
            break
    exp_history = history[pen_start_index:]

    if len(exp_history) == 0:
        # No pen trace.
        return None

    # Find the bounding box of pen trace.
    p1 = [SCREEN_WIDTH, SCREEN_HEIGHT]
    p2 = [0, 0]
    for h in exp_history:
        p1[0] = min(p1[0], h[0])
        p1[1] = min(p1[1], h[1])
        p2[0] = max(p2[0], h[0])
        p2[1] = max(p2[1], h[1])

    # Calculate image size.
    img_width = p2[0] - p1[0]
    img_height = p2[1] - p1[1]
    delta = (img_width - img_height) // 2
    if img_width > img_height:
        p1 = [p1[0], p1[1] - delta]
    else:
        p1 = [p1[0] - delta, p1[1]]
    img_width = img_height = max(img_width, img_height)

    # Draw pen trace on image.
    image = 255 * np.ones(shape=[img_width, img_height, 3], dtype=np.uint8)  # blank image with white background
    last_h = None
    for i in range(len(exp_history)):
        h = exp_history[i]
        h = (h[0] - p1[0], h[1] - p1[1])

        if last_h is None:
            last_h = h
            continue

        cv.line(image, last_h, h, (0, 0, 0), 3)  # draw line (black)
        last_h = h

    return image


def save():
    """
    Save image to file.
    :return: None
    """
    if disabled:
        return "DISABLED"

    cv.imwrite("output.png", export())
