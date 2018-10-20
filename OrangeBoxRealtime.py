import cv2
import numpy as np
from OrangeBoxGetter import GetOrangeBoxCenter

camera_matrix = np.array([[852.8381859353582, 0.0, 642.3604852739107],
                          [0.0, 849.8663434244934, 342.35385770005394],
                          [0.0, 0.0, 1.0]])
dist_coeff = np.array([0.10608960363005086, -0.14763903923715205, -0.000947508556899222, -0.004152765223021894, 0.036019737628403464])

zed_matrix = np.array([[699.555, 0, 658.919],
                       [0, 699.555, 360.179],
                      [0, 0, 1]])

dist_coeff_zed = np.array([-.16912, .021884, 0, 0])

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

zed = cv2.VideoCapture(1)
zed.set(3, 2560)
zed.set(4, 720)

while True:
    ret, frame = cap.read()
    frame = cv2.undistort(frame, camera_matrix, dist_coeff)
    ret, zedFrame = zed.read()
    zedFrame = cv2.undistort(zedFrame, zed_matrix, dist_coeff_zed)
    print(zedFrame.shape)
    zedFrame = zedFrame[:, :1280 :]
    x = GetOrangeBoxCenter(frame, "Regular Camera")
    xzed = GetOrangeBoxCenter(zedFrame, "Zed")

