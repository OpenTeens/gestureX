import cv2 as cv

# CONSTANTS
GRID_SIZE = 20  # px
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

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
    for bound_x in [x + radius, x - radius]:
        for bound_y in [y + radius, y - radius]:
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
