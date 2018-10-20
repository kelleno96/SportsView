import cv2

def GetOrangeBoxCenter(image, label):
    hueLower = 0
    hueUpper = 39
    if label == 'zed':
        hueUpper = 8
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (hueLower, 200, 0), (hueUpper, 255, 200))
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    x = False
    if (len(contours) > 0):
        largestContour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largestContour)
        cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 4)
    cv2.imshow("Image with circle" + label, image)
    cv2.waitKey(1)
    return x
