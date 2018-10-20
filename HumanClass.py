import cv2
import numpy as np
import os
from math import sin, cos, atan, tan, sqrt, pow
import matplotlib.pyplot as plt
from time import sleep

class Human:
    def __init__(self, x, y, hue, timestamp):
        self.position = (x, y)
        self.hue = hue
        self.distanceTraveled = 0
        self.timestamp = timestamp
        self.startTime = timestamp
        self.fig = plt.figure(1)
        self.ax = self.fig.add_subplot(111)
    def update(self, x, y, timestamp):
        self.distanceTraveled+= sqrt(pow(self.position[0]-x,2)+ pow(self.position[1]-y,2))
        dt = timestamp-self.timestamp
        self.position = (x, y)
        self.averageSpeed = self.distanceTraveled/dt
        print("Position: " + str(self.position))
        print("Distance: " + str(self.distanceTraveled))
        print("Average speed: " + str(self.averageSpeed))
    def visualize(self):
        self.ax.scatter((self.position[0]), (self.position[1]))
        self.ax.set_xbound(-10, 10)
        self.ax.set_ybound(-10, 10)
        plt.pause(.05)
        self.ax.cla()
