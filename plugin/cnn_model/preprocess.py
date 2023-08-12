import json
import numpy as np
from PIL import Image
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Input, Activation, Reshape
from tensorflow.keras.optimizers.legacy import Adam

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
    categories = np.array([label_to_category[label] for label in labels])
    categories = to_categorical(categories)  # Convert labels into one-hot encoding

    return images, categories

images_folder = 'dataCNN'
json_path = 'cnn_labels.json'
target_size = (224, 224)

json_data = load_json(json_path)

image_label_mapping = associate_images_with_labels(images_folder, json_data)


images, labels = prepare_data(image_label_mapping, target_size)

train_images, train_labels, test_images, test_labels = train_test_split(images, labels, test_size=0.2, random_state=42)

print(len(train_images))
print(len(train_labels))

#
# model = Sequential()
# model.add(Reshape((70, 70, 1)))
# model.add(Conv2D(70, (3, 3), padding='same'))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.3))
#
# model.add(Conv2D(70, (3, 3), padding='same'))
#
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Activation('relu'))
#
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Conv2D(70, (3, 3), padding='same'))
# model.add(Activation('relu'))
#
# model.add(Dropout(0.3))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Activation('relu'))
#
# model.add(Flatten())
#
# model.add(Dense(200))
# model.add(Activation('relu'))
# model.add(Dense(4))
# model.add(Activation('softmax'))
#
# opt = Adam(learning_rate=0.001)
#
#
# model.compile(loss='categorical_crossentropy',
#               optimizer=opt,
#               metrics=['accuracy'])
# epochs = 25
# batch_size = 32
#
# history = model.fit(train_images,train_labels, batch_size=batch_size,
#                               epochs = epochs)
#
# print(history)
#
# test_loss, test_accuracy = model.evaluate(test_images, test_labels)
#
# print(test_accuracy)