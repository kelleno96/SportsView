import cv2
import numpy as np
import os

HumanDetector = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

class Human:
    def __init__(self, x, y, hue):
        self.position = (x,y)
        self.hue = hue

def GetHumanBoxCenter(image, label):
    x = False
    height, width = image.shape[:2]
    oldWidth = width
    image = image[:, int((width-height)/2):(width-int((width-height)/2))]
    inputImage = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), .007843, (300, 300), 127.5)
    width = height
    HumanDetector.setInput(inputImage)
    humanDetections = HumanDetector.forward()
    xlist = []
    for i in range(0, humanDetections.shape[2]):
        conf = humanDetections[0, 0, i, 2]
        objectType = int(humanDetections[0, 0, i, 1])
        if objectType == 15:
            if(conf > .5):
                boundingBox = humanDetections[0, 0, i, 3:7]*np.array([width, height, width, height])
                boundingBox = boundingBox.astype("int")
                boxWidth = boundingBox[2]-boundingBox[1]
                center = boundingBox[0] + boxWidth/2
                center = int(center)
                x = center + int((oldWidth-height)/2)
                
                cv2.rectangle(image, (boundingBox[0], boundingBox[1]), (boundingBox[2], boundingBox[3]),
                              (255, 0, 200), 2)

                # get average color and then append x and color as a tuple
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                y_dif = boundingBox[3] - boundingBox[1]
                x_dif = boundingBox[2] - boundingBox[0]
                h_val = hsv[(int)(boundingBox[1]+y_dif*0.32):(int)(boundingBox[1]+y_dif*.53),(int)(boundingBox[0] + x_dif*0.1):(int)(boundingBox[2]-x_dif*.1),0].mean()
                # print("hsv value: " + str(h_val))
                cv2.rectangle(image, ((int)(boundingBox[0] + x_dif*0.1), (int)(boundingBox[1]+y_dif*0.32)), ((int)(boundingBox[2]-x_dif*.1), (int)(boundingBox[1]+y_dif*.53)),
                              (0, 255, 0), 2)
                xlist.append((x, h_val))

    cv2.imshow("image" + label, image)
    cv2.waitKey(1)
    return xlist
