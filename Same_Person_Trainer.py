from SamePersonNetwork import same_person_network
import os
from os import listdir
import cv2
import random
import keras
import numpy as np


andrewlist = []
kellenlist = []

for file in os.listdir('andrew'):
    filename = os.path.join('andrew', file)
    image = cv2.imread(filename)
    image = cv2.resize(image, (0, 0), fx=.25, fy = .25)
    andrewlist.append(image)


for file in os.listdir('kellen'):
    filename = os.path.join('kellen', file)
    image = cv2.imread(filename)
    image = cv2.resize(image, (0, 0), fx=.25, fy=.25)
    kellenlist.append(image)



X_Train = []
Y_Train = []
X_Test = []
Y_Test = []

for i in range(0, 49):
    numberIndex = random.randint(0, 48)
    pickSame = random.randint(0, 1)
    if(pickSame):
        if(i<30):
            image1 = kellenlist[numberIndex]
            image2 = kellenlist[numberIndex+1]
            image3 = andrewlist[numberIndex]
            image4 = andrewlist[numberIndex+1]
            kellenimg=np.concatenate((image1, image2), axis=2)
            andrewimg = np.concatenate((image3, image4), axis=2)
            X_Train.append(kellenimg)
            X_Train.append(andrewimg)
            y = 1
            Y_Train.append(y)
            Y_Train.append(y)
        else:
            image1 = kellenlist[numberIndex]
            image2 = kellenlist[numberIndex + 1]
            image3 = andrewlist[numberIndex]
            image4 = andrewlist[numberIndex + 1]
            kellenimg = np.concatenate((image1, image2), axis=2)
            andrewimg = np.concatenate((image3, image4), axis=2)
            X_Test.append(kellenimg)
            X_Test.append(andrewimg)
            y = 1
            Y_Test.append(y)
            Y_Test.append(y)
    else:
        if(i<30):
            image1 = kellenlist[numberIndex]
            image2 = andrewlist[numberIndex]
            bothimg = np.concatenate((image1, image2), axis=2)
            y=0
            X_Test.append(bothimg)
            Y_Test.append(y)

X_Train = np.array(X_Train).astype(dtype=np.float32)/255.0
Y_Train = np.array(Y_Train).astype(dtype=np.float32)
Y_Train = keras.utils.to_categorical(Y_Train)
X_Test = np.array(X_Train).astype(dtype=np.float32)/255.0
Y_Test = np.array(Y_Train).astype(dtype=np.float32)
Y_Test = keras.utils.to_categorical(Y_Train)
print(X_Train.shape)
print(Y_Train.shape)

spn = same_person_network(120, 160, 6)

spn.fit(X_Train, Y_Train, batch_size=5, nb_epoch=25)
