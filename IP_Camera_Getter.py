import cv2
from urllib import request
from time import sleep
import numpy as np

#cap = cv2.VideoCapture("http://10.27.165.7:8080/shot.jpg")
urlAndrew = "http://10.27.165.7:8888/shot.jpg"
urlKellen = "http://10.27.167.70:8080/shot.jpg"
usbCam = cv2.VideoCapture(0)

while True:
    ret, frame2 = usbCam.read()
    imageResp = request.urlopen(urlKellen)
    frame = np.array(bytearray(imageResp.read()), dtype=np.uint8)
    frame = cv2.imdecode(frame, -1)


    cv2.imshow("Frame", frame)
    cv2.imshow("Frame2", frame2)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
