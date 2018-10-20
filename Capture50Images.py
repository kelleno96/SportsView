import cv2

cap = cv2.VideoCapture(0)

person = 'andrew'

for i in range(0, 50):
    ret, frame = cap.read()
    filename = r"C:/Users/xpist/Google Drive/College/Semester 7/SportsView/" + person+"/"+str(i)+".png"
    print(filename)
    cv2.imwrite(filename, frame)
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)