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

plotvis = False
if(plotvis):
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

camera_matrix = np.array([[1002.3757049332412, 0.0, 687.9046880271991],
                          [0.0, 1013.1595817543699, 322.92868217922586],
                          [0.0, 0.0, 1.0]])
dist_coeff = np.array(
    [-0.05781517918727033, -0.05102773634971141, -0.003308634814107245, 0.006733503182426772,
     0.28063494684779966])

zed_matrix = np.array([[1784.283108097664, 0.0, 642.9225178970478], # For silver camera
                       [0.0, 1787.0262645268176, 360.87871534433754],
                       [0.0, 0.0, 1.0]])

dist_coeff_zed = np.array([-0.13485041724121793, 0.6660303345880927, 0.006472309177555823, -0.005318732695265743, -4.292297704139373])

cap = cv2.VideoCapture(2)
cap.set(3, 1280)
cap.set(4, 720)

zed = cv2.VideoCapture(1)
zed.set(3, 2560)
zed.set(4, 720)

# camera locations
c1_loc = (91 * 25.4, 192 * 25.4)
c2_loc = (0, 192 * 25.4)
c1_ori = -25.26 # Negative if camera at 0, 0 is turned in.
c2_ori = -25.26 # Negative if camera at (x, 0) is turned in towards middle

imageScaleFactor = 2

def match_people_hsv(reg_ppl, zed_ppl):

    matches = []

    for rppl in reg_ppl:
        for zppl in zed_ppl:
            if(abs(rppl[1] - zppl[1]) < 20):
                matches.append((rppl, zppl))
            else:
                pass
                # print("hue difference: " + str(abs(rppl[1]-zppl[1])))

    return matches

packetList = []
while 1:

    # get two images
    ret, frame = cap.read()
    frame = cv2.undistort(frame, camera_matrix, dist_coeff)
    ret, zedFrame = zed.read()
    zedFrame = cv2.undistort(zedFrame, zed_matrix, dist_coeff_zed)
    zedFrame = zedFrame[:, :1280:]


    x = GetHumanBoxCenter(frame, "Regular Camera")
    xzed = GetHumanBoxCenter(zedFrame, "Zed/silver camera")
    ballx_regular = GreenBallTracker(frame, "ballreg")
    ballx_zed = GreenBallTracker(zedFrame, "Ballzed")

    if (not x or not xzed):
    	continue
    # put boxes around and get coordinates
    x_loc_l = x
    x_loc_r = xzed
    Cx = camera_matrix[0][2]
    Fx = camera_matrix[0][0]
    CxZed = zed_matrix[0][2]
    FxZed = zed_matrix[0][0]

    # ip = '10.27.255.254'
    # port = 8080
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((ip, port))
    # s.send("test")
    # s.close()

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

        delta_x = abs(c1_loc[0] - 0)/1000
        delta_y = abs(c1_loc[1] - 0)/1000

        y_loc_ball = delta_y - (B * sin(radians(alpha)) / 1000)
        x_loc_ball = delta_x - (B * cos(radians(alpha)) / 1000)

        packet = {"x_pos":x_loc_ball, 
                  "y_pos":y_loc_ball, 
                  "hue":(-1.0), 
                  "time":str(datetime.datetime.utcnow())}

        headers = {'Content-Type':'application/json'}
        r = requests.post("https://xkscasu3ie.execute-api.us-east-2.amazonaws.com/api/data", data=json.dumps(packet), headers=headers)
       
        print("Ball:  x, y: " + str(x_loc_ball) + ", " + str(y_loc_ball))
        if (plotvis):
            ax.scatter(x_loc_ball, y_loc_ball, s=10, c='g')
            ax.set_xbound(0, 10)
            ax.set_ybound(0, 10)
            ax.set_aspect('equal')

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
        # print("B: " + str(B) + " A: " + str(A))
        delta_x = abs(c1_loc[0] - 0)/1000
        delta_y = abs(c1_loc[1] - 0)/1000

        # print("delta_x = " + str(delta_x) + " delta_y = " + str(delta_y))
        # print("x loc: " + str(B * sin(radians(alpha))/1000) + " y loc: " + str(B * cos(radians(alpha))/1000))
        y_loc_obj = delta_y - (B * sin(radians(alpha))/1000)
        x_loc_obj = delta_x - (B * cos(radians(alpha))/1000)

        # print("object #" + str(i) + " x, y: " + str("%0.2f" % x_loc_obj) + ", " + str("%0.2f" % y_loc_obj))
        if(plotvis):
            ax.scatter(x_loc_obj, y_loc_obj, s = 10, c = 'r')
            ax.set_xbound(0, 10)
            ax.set_ybound(0, 10)
            ax.set_aspect('equal')
            plt.pause(.05)

        # x = [c1_loc[0], c2_loc[0], (x_loc_o bj)]
        # y = [c1_loc[1], c2_loc[1], (y_loc_obj)]
        i+= 1

        # send the x, y location and average hue and time
        packet = {"x_pos":x_loc_obj, 
                  "y_pos":y_loc_obj, 
                  "hue":((match[0][1] + match[1][1])/2), 
                  "time":str(datetime.datetime.utcnow())}
        # packetList.append(packet)
        #if(len(packetList)==5):
        headers = {'Content-Type':'application/json'}
        r = requests.post("https://xkscasu3ie.execute-api.us-east-2.amazonaws.com/api/data", data=json.dumps(packet), headers=headers)
        # print("SENT PACKET********************************************************************")
        packetList = []
    plt.pause(.05)