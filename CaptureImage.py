import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
ret, frame = cap.read()
cv2.imshow("Frame", frame)
cv2.waitKey(0)
#cv2.imwrite("right.png", frame)