import tensorflow as tf
from tensorflow.keras.layers import *

output_labels = [
  'other',     #    0
  'ellipse',   #    1
  'rectangle', #    2
  'triangle']  #    3

num_classes = 4

model = Sequential()
model.add(Reshape((32, 32, 3)))
model.add(Conv2D(32, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

model.add(Conv2D(75, (3, 3), padding='same')) 

model.add(MaxPooling2D(pool_size=(2, 2))) 
model.add(Activation('relu'))

model.add(Dense(256))

model.add(MaxPooling2D(pool_size=(2, 2))) #pooling layer usually helps with overfitting
model.add(Conv2D(70, (3, 3), padding='same')) 
model.add(Activation('relu'))

model.add(Dropout(0.5))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Activation('relu'))

model.add(Flatten())

model.add(Dense(512))
opt = tf.keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)


model.compile(loss='categorical_crossentropy',
              optimizer=opt, 
              metrics=['accuracy'])

history = model.fit(inputs_train, labels_train, \
                    validation_data=(inputs_test, labels_test), \
                    epochs=100)


