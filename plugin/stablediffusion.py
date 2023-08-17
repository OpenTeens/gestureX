import os
import threading
import tkinter as tk

import cv2 as cv
import plugin.blackboard
import requests

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
generating_image = False


def generate_image():
    """
    Generate stable diffusion image using blackboard sketch
    :return: None
    """

    global generating_image

    def helper():
        def gen_img():
            global generating_image
            name = input_entry.get()
            window.destroy()

            RapidAPI_Key = "cb471ed932msh450278f2d7a8b04p132186jsn56f926ff717b"
            url = "https://dezgo.p.rapidapi.com/image2image"
            prompt = f"draw a {name} with appropriate color"
            negative_prompt = ""
            filename = "sd_input.png"

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

            plugin.blackboard.save(1)

            response = requests.post(url, data=payload, files=files, headers=headers)
            if response.status_code == 200:
                with open("result.png", "wb") as file:
                    file.write(response.content)
            else:
                print(response.status_code)
            generating_image = False
            plugin.blackboard.clear()

        window = tk.Tk()
        window.title("SD - gestureX")

        input_entry = tk.Entry(window, width=30)
        input_entry.grid(row=0, column=0)
        tk.Button(window, width=10, height=1, text="Submit", command=gen_img).grid(row=0, column=1)
        tk.Button(window, width=10, height=1, text="Clear", command=lambda: input_entry.delete(0, tk.END)).grid(row=1,
                                                                                                                  column=1)
        window.mainloop()

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
    # for i in range(len(img)):
    #     for j in range(len(img[0])):
    #         background[y + i][x + j] = img[i][j]
    background[y:y + len(img), x:x + len(img[0])] = img
