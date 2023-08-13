import requests
import cv2 as cv
import os

def generate_image(name):
    """
    Generate stable diffusion image using blackboard sketch
    :param name: name of the drawn object 
    :return: True if success, False if failed
    """
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