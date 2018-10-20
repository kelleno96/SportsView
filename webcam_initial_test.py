import socket
import cv2
from math import *

import numpy as np
from OrangeBoxGetter import GetOrangeBoxCenter

camera_matrix = np.array([[852.8381859353582, 0.0, 642.3604852739107],
                          [0.0, 849.8663434244934, 342.35385770005394],
                          [0.0, 0.0, 1.0]])
dist_coeff = np.array(
    [0.10608960363005086, -0.14763903923715205, -0.000947508556899222, -0.004152765223021894, 0.036019737628403464])

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

# camera locations
c1_loc = (0, 0)
c2_loc = (73.5 * 25.4, 0)

while 1:
    # get two images
    ret, frame = cap.read()
    frame = cv2.undistort(frame, camera_matrix, dist_coeff)
    ret, zedFrame = zed.read()
    zedFrame = cv2.undistort(zedFrame, zed_matrix, dist_coeff_zed)
    zedFrame = zedFrame[:, :1280:]
    x = GetOrangeBoxCenter(frame, "Regular Camera")
    xzed = GetOrangeBoxCenter(zedFrame, "Zed")

    # put boxes around and get coordinates

    # x_loc_l = 803
    # y_loc_l = 53
    # x_loc_r = 624
    # y_loc_r = 23
    x_loc_l = x
    x_loc_r = xzed
    Cx = 642
    Fx = 852.83
    CxZed = 658.919
    FxZed = 699.555

    # figure out location

    beta = 90 - degrees(atan(abs(x_loc_r - CxZed) / FxZed))
    alpha = 90 - degrees(atan(abs(x_loc_l - CxZed) / FxZed))

    # print(beta)
    # print(alpha)
    # print(abs(c1_loc[0] - c2_loc[0]))
    # print(degrees(sin(radians(beta))))
    B = (abs(c1_loc[0] - c2_loc[0])) * sin(radians(beta)) / sin(radians(180 - alpha - beta))
    A = (abs(c1_loc[0] - c2_loc[0])) * sin(radians(alpha)) / sin(radians(180 - alpha - beta))

    y_loc_obj = B * sin(radians(alpha))
    x_loc_obj = B * cos(radians(alpha))

    print("x, y: " + str(x_loc_obj / 1000) + ", " + str(y_loc_obj / 1000))

