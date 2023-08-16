from tensorflow import keras
import cnn
import json
from sklearn.model_selection import train_test_split

images_folder = 'plugin/cnn_model/dataCNN'
json_path = 'plugin/cnn_model/cnn_labels.json'
json_data = cnn.load_json(json_path)
target_size = (224, 224)


image_label_mapping = cnn.associate_images_with_labels(images_folder, json_data)
images, labels = cnn.prepare_data(image_label_mapping, target_size)

# split data set into training and testing data sets
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.2, random_state=42)
model = keras.models.load_model("plugin/cnn_model/model.keras")

test_loss, test_accuracy = model.evaluate(test_images, test_labels)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

