import requests
import cv2 as cv
import threading
import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
generating_image = False


def generate_image(name):
    """
    Generate stable diffusion image using blackboard sketch
    :param name: name of the drawn object
    :return: True if success, False if failed
    """

    global generating_image
    RapidAPI_Key = os.getenv("RapidAPI_Key")
    url = "https://dezgo.p.rapidapi.com/image2image"
    prompt = f"draw a {name} with appropriate color"
    negative_prompt = ""
    filename = "input.png"

    files = {'init_image': open(filename, 'rb')}
    payload = {
        "upscale": "1",
        "prompt": prompt,
        "steps": "30",
        "sampler": "euler_a",
        "negative_prompt": negative_prompt,
        "model": "epic_diffusion_1_1",
        "strength": "0.6",
        "guidance": "7"
    }
    headers = {
        "X-RapidAPI-Key": RapidAPI_Key,
        "X-RapidAPI-Host": "dezgo.p.rapidapi.com"
    }

    def helper():
        global generating_image
        response = requests.post(url, data=payload, files=files, headers=headers)
        if response.status_code == 200:
            with open("result.png", "wb") as file:
                file.write(response.content)
        else:
            print(response.status_code)
        generating_image = False

    generating_image = True
    threading.Thread(target=helper).start()


def clear():
    """
    Clear image by deleting the file
    :return: None
    """
    if os.path.exists("result.png"):
        os.remove("result.png")


def render_image_overlay(background, pos, scale=1):
    """
    Overlay the stable diffusion image on webcam
    :param background: webcam/cv input
    :param pos: top left position of overlaying image
    :return: if failed
    """
    if not os.path.exists("result.png"):
        return
    else:
        img = cv.imread("result.png")
    x = pos[0]
    y = pos[1]
    img = cv.resize(img, (0, 0), fx=scale, fy=scale)
    for i in range(len(img)):
        for j in range(len(img[0])):
            background[y + i][j + x] = img[i][j]
