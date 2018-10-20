import socket
import cv2
from math import *
import numpy as np
from OrangeBoxGetter import GetOrangeBoxCenter
import matplotlib.pyplot as plt
from HumanBoxGetter import GetHumanBoxCenter

camera_matrix = np.array([[852.8381859353582, 0.0, 642.3604852739107],
                          [0.0, 849.8663434244934, 342.35385770005394],
                          [0.0, 0.0, 1.0]])
dist_coeff = np.array(
    [0.10608960363005086, -0.14763903923715205, -0.000947508556899222, -0.004152765223021894, 0.036019737628403464])

zed_matrix = np.array([[699.555, 0, 658.919],
                       [0, 699.555, 360.179],
                       [0, 0, 1]])

dist_coeff_zed = np.array([-.16912, .021884, 0, 0])

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

zed = cv2.VideoCapture(2)
zed.set(3, 2560)
zed.set(4, 720)

# camera locations
c1_loc = (0, 0)
c2_loc = (30.5 * 25.4, 0)
c1_ori = 0.0
c2_ori = 0.0

fig = plt.figure()
fig.add_subplot(111);
imageScaleFactor = 2

def match_people_hsv(reg_ppl, zed_ppl):

    matches = []

    for rppl in reg_ppl:
        for zppl in zed_ppl:
            if(abs(rppl[1] - zppl[1]) < 20):
                matches.append((rppl, zppl))

    return matches

while 1:

    # get two images
    ret, frame = cap.read()
    frame = cv2.undistort(frame, camera_matrix, dist_coeff)
    ret, zedFrame = zed.read()
    zedFrame = cv2.undistort(zedFrame, zed_matrix, dist_coeff_zed)
    zedFrame = zedFrame[:, :1280:]


    x = GetHumanBoxCenter(frame, "Regular Camera")
    xzed = GetHumanBoxCenter(zedFrame, "Zed")

    if (not x or not xzed):
    	continue
    # put boxes around and get coordinates
    x_loc_l = x
    x_loc_r = xzed
    Cx = 642
    Fx = 852.83
    CxZed = 658.919
    FxZed = 699.555

    # match up people base on hue similarity
    matches = match_people_hsv(x, xzed)

    i = 0
    for match in matches:
        # figure out location
        beta = 0
        alpha = 0
        theta_u_right = degrees(atan(abs(match[1][0] - CxZed) / FxZed))
        if match[1][0] - CxZed < 0:
        	beta = 90 - theta_u_right
        else:
        	beta = 90+ theta_u_right

        theta_u_left = degrees(atan(abs(match[0][0] - Cx) / Fx))
        if match[0][0] - Cx > 0:
        	alpha = 90 - theta_u_left
        else:
        	alpha = 90 + theta_u_left

        alpha += c1_ori
        beta += c2_ori

        B = (abs(c1_loc[0] - c2_loc[0])) * sin(radians(beta)) / sin(radians(180 - alpha - beta))
        A = (abs(c1_loc[0] - c2_loc[0])) * sin(radians(alpha)) / sin(radians(180 - alpha - beta))

        y_loc_obj = B * sin(radians(alpha))/1000
        x_loc_obj = B * cos(radians(alpha))/1000

        print("obecjt #" + str(i) + " x, y: " + str(x_loc_obj) + ", " + str(y_loc_obj))

        x = [c1_loc[0], c2_loc[0], (x_loc_obj)]
        y = [c1_loc[1], c2_loc[1], (y_loc_obj)]
        i+= 1