import json
import os

data = []

list = ["Ellipse", "Rectangle", "Triangle"]

for i in range(3):
    tag = list[i]
    folder_path = f"dataCNN/{tag}"

    for file_name in os.listdir(folder_path):
        if file_name.endswith((".png", ".jpg", ".jpeg")):
            image_name = os.path.splitext(file_name)[0] + ".png"
            data2 = {}
            data2['filename'] = image_name
            data2['label'] = tag

            data.append(data2)

json_data = json.dumps(data)

with open("cnn_labels.json", "w") as file:
    file.write(json_data)

print("JSON data has been written to 'data.json' file.")
