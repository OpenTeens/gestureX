from tensorflow import keras
from PIL import Image
import numpy as np

model = keras.models.load_model("model.keras")

target_size = (224, 224)

labels = {0: 'Ellipse', 1: 'Rectangle', 2:'Triangle'}

path = 'test.png'
input_data = Image.open(path).resize(target_size)
input_data = input_data.convert('RGB')
input_data = np.array(input_data) / 255.0
input_data = np.expand_dims(input_data, axis=0)  # Add a batch dimension
print(input_data.shape)
prediction = model.predict(input_data)
prediction = np.argmax(prediction) # find the highest probability
print(labels[prediction])
