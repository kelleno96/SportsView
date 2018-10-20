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
    numSegments = 3
    height, width = image.shape[:2]
    sliceWidth = int(width/numSegments)
    x_detections = []
    for i in range(0, numSegments):
        slice = input[:, i*sliceWidth:(i+1)*sliceWidth-1]
        inputImage = cv2.dnn.blobFromImage(cv2.resize(slice, (300, 300)), .007843, (300, 300), 127.5)
        HumanDetector.setInput(inputImage)
        humanDetections = HumanDetector.forward()
        for i in range(0, humanDetections.shape[2]):
            conf = humanDetections[0, 0, i, 2]
            objectType = int(humanDetections[0, 0, i, 1])
            if objectType == 15:
                if(conf > .7):
                    boundingBox = humanDetections[0, 0, i, 3:7]*np.array([width, height, width, height])
                    boundingBox = boundingBox.astype("int")
                    width = boundingBox[2]-boundingBox[1]
                    center = boundingBox[0] + width/2
                    center = int(center)
                    x = center + i*sliceWidth
                    x_detections.append(x)
                    cv2.rectangle(image, (boundingBox[0]+i*sliceWidth, boundingBox[1]), (boundingBox[2]+i*sliceWidth, boundingBox[3]),
                                  (255, 0, 200), 2)
    cv2.imshow("image" + label, image)
    cv2.waitKey(1)
    return x_detections
