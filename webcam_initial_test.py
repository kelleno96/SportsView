import socket
import cv2
from math import *

camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(1)

# camera locations
c1_loc = (0, 0)
c2_loc = (31*25.4, 0)

while 1:

	# get two images
	res1, image1 = camera1.read()
	res2, image2 = camera2.read()

	# put boxes around and get coordinates

	x_loc_l = 803;
	y_loc_l = 53;
	x_loc_r = 624;
	y_loc_r = 23;
	Cx = 642;
	Fx = 850;

	# figure out location

	beta = 90 - degrees(atan(abs(x_loc_r - Cx) / Fx))
	alpha = 90 - degrees(atan(abs(x_loc_l - Cx) / Fx))

	print(beta)
	print(alpha)
	print(abs(c1_loc[0] - c2_loc[0]))
	print(degrees(sin(radians(beta))))
	B = (abs(c1_loc[0] - c2_loc[0])) * sin(radians(beta)) / sin(radians(180 - alpha - beta))
	A = (abs(c1_loc[0] - c2_loc[0])) * sin(radians(alpha)) / sin(radians(180 - alpha - beta))

	y_loc_obj = B * sin(radians(alpha))
	x_loc_obj = B * cos(radians(alpha))

	print("x location is: ")
	print(x_loc_obj / 1000)
	print("y location is: ")
	print(y_loc_obj / 1000)

	break


