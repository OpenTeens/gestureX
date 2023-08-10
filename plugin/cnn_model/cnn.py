# https://github.com/frobertpixto/hand-drawn-shapes-dataset

import pickle
import os
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Input, Activation, Reshape
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

BASEDIR = ".."
PICKLE_DIR     = os.path.join(BASEDIR, 'pickles')
TRAIN_DATAFILE = os.path.join(PICKLE_DIR, 'train.pickle')
VAL_DATAFILE   = os.path.join(PICKLE_DIR, 'val.pickle')
TEST_DATAFILE  = os.path.join(PICKLE_DIR, 'test.pickle')

output_labels = [
  'other',     #    0
  'ellipse',   #    1
  'rectangle', #    2
  'triangle']  #    3

num_classes = 4

with open(TRAIN_DATAFILE, 'rb') as file:
    train_dict = pickle.load(file)
with open(VAL_DATAFILE, 'rb') as file:
    val_dict = pickle.load(file)
with open(TEST_DATAFILE, 'rb') as file:
    test_dict = pickle.load(file)

train_X = train_dict['train_data']
train_y = train_dict['train_labels']

val_X = val_dict['val_data']
val_y = val_dict['val_labels']

# image size is 70
X_train = train_X.reshape(-1,70,70,1)
X_val   = val_X.reshape(-1,70, 70, 1)

Y_train = to_categorical(train_y, num_classes = num_classes)
Y_val   = to_categorical(val_y, num_classes = num_classes)


model = Sequential()
model.add(Reshape((70, 70, 1)))
model.add(Conv2D(70, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

model.add(Conv2D(70, (3, 3), padding='same'))

model.add(MaxPooling2D(pool_size=(2, 2))) 
model.add(Activation('relu'))

model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(70, (3, 3), padding='same')) 
model.add(Activation('relu'))

model.add(Dropout(0.3))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Activation('relu'))

model.add(Flatten())

model.add(Dense(200))
model.add(Activation('relu'))
model.add(Dense(4))
model.add(Activation('softmax'))



opt = Adam(lr=2e-3, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0, amsgrad=False)


model.compile(loss='categorical_crossentropy',
              optimizer=opt, 
              metrics=['accuracy'])

epochs = 25
batch_size = 32

history = model.fit(X_train,Y_train, batch_size=batch_size,
                              epochs = epochs, validation_data = (X_val,Y_val))




