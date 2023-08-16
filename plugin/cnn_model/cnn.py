import json
import numpy as np
from PIL import Image
from tensorflow import keras
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Input, \
    Activation, Reshape
from tensorflow.keras.optimizers import legacy as keras_legacy_optimizer
from tensorflow.keras.layers import Reshape
import tensorflow as tf
from tensorflow import keras
import pickle


def preprocess_image(image_path, target_size):
    image = Image.open(image_path)
    image = image.resize(target_size)
    image = image.convert('RGB')
    image = np.array(image) / 255.0
    return image


def load_json(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    return json_data


def associate_images_with_labels(images_folder, json_data):
    image_label_mapping = {}
    for item in json_data:
        image_filename = item['filename']
        image_label = item['label']
        image_path = os.path.join(images_folder, image_filename)
        image_label_mapping[image_path] = image_label
    return image_label_mapping


def prepare_data(image_label_mapping, target_size):
    images = []
    labels = []

    for image_path, label in image_label_mapping.items():
        image = preprocess_image(image_path, target_size)
        images.append(image)
        labels.append(label)

    images = np.array(images)
    labels = np.array(labels)

    # Encode the labels numerically
    unique_labels = np.unique(labels)
    label_to_category = {label: category for category, label in enumerate(unique_labels)}
    # print(label_to_category)
    categories = np.array([label_to_category[label] for label in labels])
    categories = to_categorical(categories)  # Convert labels into one-hot encoding

    return images, categories


# read the data from the folder
images_folder = 'plugin/cnn_model/dataCNN'
json_path = 'plugin/cnn_model/cnn_labels.json'
target_size = (224, 224) # size of the reshape

json_data = load_json(json_path)

# preprocess data
image_label_mapping = associate_images_with_labels(images_folder, json_data)
images, labels = prepare_data(image_label_mapping, target_size)

# print(labels)

# split data set into training and testing data sets
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.2, random_state=42)

# building the model: CNN with convolution layer, pooling, and dense
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(filters=64, kernel_size=7, input_shape=[224, 224, 3]),
    tf.keras.layers.MaxPooling2D(pool_size=2),
    tf.keras.layers.Conv2D(filters=128, kernel_size=3, activation='relu', padding="SAME"),
    tf.keras.layers.MaxPooling2D(pool_size=2),
    tf.keras.layers.Conv2D(filters=128, kernel_size=3, activation='relu', padding="SAME"),
    tf.keras.layers.MaxPooling2D(pool_size=2),
    tf.keras.layers.Conv2D(filters=128, kernel_size=3, activation='relu', padding="SAME"),
    tf.keras.layers.MaxPooling2D(pool_size=2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=128, activation='relu'),
    tf.keras.layers.Dropout(0.3), # data dropout
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(units=3, activation='softmax'),
    # output layer: labels = {0: 'Ellipse', 1: 'Rectangle', 2: 'Triangle'}
])

opt = keras_legacy_optimizer.Adam(learning_rate=0.001)

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

epochs = 4
batch_size = 32

history = model.fit(train_images, train_labels, batch_size=batch_size, epochs=epochs)

print(history)

test_loss, test_accuracy = model.evaluate(test_images, test_labels)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

model.save("plugin/cnn_model/model.keras", save_format='keras')

