import socket
import cv2
from math import *
import numpy as np
from OrangeBoxGetter import GetOrangeBoxCenter
import matplotlib.pyplot as plt
from HumanBoxGetter import GetHumanBoxCenter
import requests
import json
import datetime
from GreenBallTracker import GreenBallTracker
import matplotlib.pyplot as plt

plotvis = True
if(plotvis):
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

camera_matrix = np.array([[852.8381859353582, 0.0, 642.3604852739107],
                          [0.0, 849.8663434244934, 342.35385770005394],
                          [0.0, 0.0, 1.0]])
dist_coeff = np.array(
    [0.10608960363005086, -0.14763903923715205, -0.000947508556899222, -0.004152765223021894, 0.036019737628403464])

zed_matrix = np.array([[1784.283108097664, 0.0, 642.9225178970478],
                       [0.0, 1787.0262645268176, 360.87871534433754],
                        [0.0, 0.0, 1.0]])

dist_coeff_zed = np.array([-0.13485041724121793, 0.6660303345880927, 0.006472309177555823, -0.005318732695265743, -4.292297704139373])

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

zed = cv2.VideoCapture(2)
zed.set(3, 1280)
zed.set(4, 720)

# camera locations
c1_loc = (0, 0)
c2_loc = (36 * 25.4, 0)
c1_ori = 0.0
c2_ori = 0.0

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


    x = GetHumanBoxCenter(frame, "Regular Camera")
    xzed = GetHumanBoxCenter(zedFrame, "Zed")
    ballx_regular = GreenBallTracker(frame, "ballreg")
    ballx_zed = GreenBallTracker(zedFrame, "Ballzed")

    if (not x or not xzed):
    	continue
    # put boxes around and get coordinates
    x_loc_l = x
    x_loc_r = xzed
    Cx = 642
    Fx = 852.83

    CxZed = zed_matrix[0][2]
    FxZed = zed_matrix[0][0]

    # match up people base on hue similarity
    matches = match_people_hsv(x, xzed)
    if (ballx_zed and ballx_regular):
        beta = 0
        alpha = 0
        theta_u_right = degrees(atan(abs(ballx_zed - CxZed) / FxZed))
        if ballx_zed - CxZed < 0:
            beta = 90 - theta_u_right
        else:
            beta = 90 + theta_u_right

        theta_u_left = degrees(atan(abs(ballx_regular - Cx) / Fx))
        if ballx_regular - Cx > 0:
            alpha = 90 - theta_u_left
        else:
            alpha = 90 + theta_u_left

        alpha += c1_ori
        beta += c2_ori

        B = (abs(c1_loc[0] - c2_loc[0])) * sin(radians(beta)) / sin(radians(180 - alpha - beta))
        A = (abs(c1_loc[0] - c2_loc[0])) * sin(radians(alpha)) / sin(radians(180 - alpha - beta))

        y_loc_ball = B * sin(radians(alpha)) / 1000
        x_loc_ball = B * cos(radians(alpha)) / 1000
        if(y_loc_ball > 0):
            print("Ball:  x, y: " + str(x_loc_ball) + ", " + str(y_loc_ball))

        # x = [c1_loc[0], c2_loc[0], (x_loc_obj)]
        # y = [c1_loc[1], c2_loc[1], (y_loc_obj)]

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

        print("object #" + str(i) + " x, y: " + str(x_loc_obj) + ", " + str(y_loc_obj))
        if(plotvis):
            ax.scatter(x_loc_obj, y_loc_obj, s = 20, c = 'r')
            ax.set_xbound(-1, 4)
            ax.set_ybound(0, 8)
            ax.set_aspect('equal')
            plt.pause(.05)

        # x = [c1_loc[0], c2_loc[0], (x_loc_obj)]
        # y = [c1_loc[1], c2_loc[1], (y_loc_obj)]
        i+= 1

        # send the x, y location and average hue and time
        packet = {"x_pos":x_loc_obj, 
                  "y_pos":y_loc_obj, 
                  "hue":((match[0][1] + match[1][1])/2), 
                  "time":str(datetime.datetime.utcnow())}
        headers = {'Content-Type':'application/json'}
        r = requests.post("https://xkscasu3ie.execute-api.us-east-2.amazonaws.com/api/data", data=json.dumps(packet), headers=headers)