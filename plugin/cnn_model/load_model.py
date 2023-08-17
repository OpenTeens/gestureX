'''
Load Model: (Step 4)
- 从 model.keras 加载模型
- 识别出 cnn_input.png 的图形，并且生成对应形状。
'''


from tensorflow import keras
from PIL import Image
import numpy as np
import plugin.blackboard


def generate_shape(paras, p1, p2):
    """
    Generate shape using CNN model
    :param paras: image paras
    :param p1: left-top point
    :param p2: right-bottom point
    :return: None
    """
    model = keras.models.load_model("plugin/cnn_model/model.keras")

    target_size = (224, 224)

    labels = {0: 'Ellipse', 1: 'Rectangle', 2: 'Triangle'}

    pname = 'cnn_input.png'
    path = f'plugin/cnn_model/{pname}'  # path of the image you are testing

    input_data = Image.open(path).resize(target_size)
    input_data = input_data.convert('RGB')
    input_data = np.array(input_data) / 255.0
    input_data = np.expand_dims(input_data, axis=0)  # Add a batch dimension
    prediction = model.predict(input_data)
    probability = np.max(prediction)  # find the highest probability
    prediction = np.argmax(prediction)  # find the highest probability

    if probability < 0.8:
        print("Shape-Reco: Other Shapes")
        return "Other Shapes"

    plugin.blackboard.delete_last_trace()
    print("Shape-Reco:", labels[prediction])
    plugin.blackboard.history_shapes.append([(p1, p2), labels[prediction].lower(), paras])
