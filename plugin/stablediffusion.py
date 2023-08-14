import requests
import cv2 as cv
import time
import os

def generate_image(name):
    """
    Generate stable diffusion image using blackboard sketch
    :param name: name of the drawn object 
    :return: True if success, False if failed
    """
    os.environ["RapidAPI_Key"] = "cb471ed932msh450278f2d7a8b04p132186jsn56f926ff717b"
    RapidAPI_Key = os.getenv("RapidAPI_Key")
    url = "https://dezgo.p.rapidapi.com/image2image"
    prompt = f"draw a {name} with approiate color"
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

    response = requests.post(url, data=payload,files=files, headers=headers)
    if response.status_code == 200:
        with open("result.png","wb") as file:
            file.write(response.content)
        return True
    else:
        print(response.status_code)
        return False
def clear():
    """
    Clear image by deleting the file
    :return: None
    """
    os.remove("result.png")
def render_image_overlay(background, pos, scale = 1):
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
    x=pos[0]
    y=pos[1]
    img=cv.resize(img,(0,0),fx=scale,fy=scale)
    for i in range(len(img)):
        for j in range(len(img[0])):
            background[y+i][j+x] = img[i][j]