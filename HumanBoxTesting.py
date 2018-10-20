import cv2
from HumanBoxGetter import GetHumanBoxCenter

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)


while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx = .5, fy = .5)
    x = GetHumanBoxCenter(frame, 'regularcam')
    if(x):
        print(x/.5)