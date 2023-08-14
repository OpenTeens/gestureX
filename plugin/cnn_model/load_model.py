from tensorflow import keras
from PIL import Image

model = keras.models.load_model("model.keras")

path = 'test.png'
input_data = Image.open(path)
prediction = model.predict(input_data)

print(prediction)

