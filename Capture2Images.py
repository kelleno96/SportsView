import cv2
import numpy as np

camera_matrix = np.array([[852.8381859353582, 0.0, 642.3604852739107],
                          [0.0, 849.8663434244934, 342.35385770005394],
                          [0.0, 0.0, 1.0]])
dist_coeff = np.array([0.10608960363005086, -0.14763903923715205, -0.000947508556899222, -0.004152765223021894, 0.036019737628403464])
fx = camera_matrix[0][0]
fy = camera_matrix[1][1]
cx = camera_matrix[0][2]
cy = camera_matrix[1][2]


def nothing():
    return
val = 5
left = cv2.imread("left.png")
right = cv2.imread("right.png")
left = cv2.undistort(left, camera_matrix, dist_coeff)
right = cv2.undistort(right, camera_matrix, dist_coeff)
cv2.namedWindow('left', cv2.WINDOW_NORMAL)
cv2.namedWindow('right', cv2.WINDOW_NORMAL)
cv2.createTrackbar('hello', 'right', val, 5, nothing)
cv2.imshow("left", left)
cv2.imshow("right", right)
cv2.waitKey(0)