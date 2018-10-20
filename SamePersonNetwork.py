import cv2
from keras.layers import Conv2D, MaxPool2D, Dense
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

def same_person_network(rows, cols, depth):
    model = Sequential()
    model.add(Conv2D(32, (3,3), activation='relu', input_shape=(rows, cols, depth)))
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPool2D(2,2))
    #model.add(Dropout(.25))
    model.add(Conv2D(128, (3,3), activation='relu'))
    model.add(Conv2D(256, (3,3), activation='relu'))
    model.add(MaxPool2D(2,2))
    model.add(Flatten())
    #model.add(Dropout(.25))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(2, activation='softmax'))
    model.compile(optimizer='adadelta', loss="categorical_crossentropy", metrics=['accuracy'])
    return model