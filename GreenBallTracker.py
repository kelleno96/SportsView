import cv2
import numpy as np

def GreenBallTracker(image, label):
    x = False
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsvLower = (75, 100 ,20)
    hsvUpper = (95, 230, 245)
    mask = cv2.inRange(hsv, hsvLower, hsvUpper)
    mask = cv2.erode(mask, None, iterations = 1)
    mask = cv2.dilate(mask, None, iterations = 2)
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(contours)>0:
        ballContour = max(contours, key=cv2.contourArea)
        ((ballX, ballY), ballRadius) = cv2.minEnclosingCircle(ballContour)
        if ballRadius > 10:
            x = ballX
    # cv2.imshow("Mask" + label, mask)
    # cv2.waitKey(1)
    return x