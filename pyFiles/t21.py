# -*- coding: utf-8 -*-
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import time
import cv2
import numpy as np
import sys
sys.path.insert(0, '/home/pi/ws')
import movement_func  as move_py
import os
import json
import argparse
import imutils

def pyDie(video_capture):
	video_capture.release()
	cv2.destroyAllWindows()
	sys.exit()
	return

def doStopProcedure():
	print("ROBOT STOPPING")
	move_py.movement_func(1)
	time.sleep(0.8)
	move_py.movement_func(99)
	time.sleep(3)
	return

def doTurnAroundProcedure():
	print("ROBOT TURNING AROUND")
	move_py.movement_func(1)
	time.sleep(0.15)
	move_py.movement_func(8)
	#time.sleep(3)
	return

def redCheck(frame):
	#::FOR RED (H, S, V)
	rangeMinRed = np.array([0, 1, 0], np.uint8)
	rangeMaxRed = np.array([10, 255, 255], np.uint8)
	centerX = -1
	centerY = -1
	width = 0
	height = 0
	rect_angle = 0
	
	imgThreshRed = cv2.inRange(frame, rangeMinRed, rangeMaxRed)

	### RED DETECTION
	_,contoursRed, hierarchyRed = cv2.findContours(imgThreshRed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	areasRed = [cv2.contourArea(c) for c in contoursRed]
	
	foundRed = False
	if np.any(areasRed):
		foundRed = True
		max_index = np.argmax(areasRed)
		cnt=contoursRed[max_index]
		
		(centerX, centerY), (width, height), rect_angle = cv2.minAreaRect(cnt)
		#insert dimension condition here
	
	return (foundRed, centerX, centerY, width, height, rect_angle)

def laneCheck(frame):
	#::FOR BLUE (H, S, V)
	rangeMin = np.array([100, 160, 0], np.uint8)
	rangeMax = np.array([140, 255, 255], np.uint8)
	centerX = -1
	centerY = -1
	width = 0
	height = 0
	rect_angle = 0
	imgThresh = cv2.inRange(frame, rangeMin, rangeMax)
	
	_, contours, hierarchy = cv2.findContours(imgThresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	areas = [cv2.contourArea(c) for c in contours]
	
	foundLane = False
	if np.any(areas):
		foundLane = True
		allTry = 1
		max_index = np.argmax(areas)
		cnt=contours[max_index]
		(centerX, centerY), (width, height), rect_angle = cv2.minAreaRect(cnt)

	
	return (foundLane, centerX, centerY, width, height, rect_angle)

####### VARIABLES #########
Kernel_size=15
low_threshold=40
high_threshold=120

rho=10
threshold=15
theta=np.pi/180
minLineLength=100
maxLineGap=1

#Stop Movement
move_py.movement_func(99)
#Kill any instance of the application
#0 = STOP | 1 = GO | 2 = PAUSE
autoFile = open("masterOff.txt","w")
autoFile.write('0')
autoFile.close()
time.sleep(2)
autoFile = open("masterOff.txt","w")
autoFile.write('1')
autoFile.close()

####### START STREAM #########
video_capture = WebcamVideoStream(src='http://127.0.0.1:8081/').start()

print(sys.argv[1])
if len(sys.argv) > 1:
	definedStops = json.loads(sys.argv[1])
	numberOfStops = int(sys.argv[2])
else:
	print("Not enough parameters given. Exiting")
	pyDie(video_capture)

while True:
	#start capturing frames for processing
	frame = video_capture.read()
	orig = imutils.resize(frame, width=400)
	frame = orig
	difference = 0
	imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	
	foundLane, centerX, centerY, width, height, rect_angle = laneCheck(imgHSV)
	foundRed, centerX, centerY, width, height, rect_angle = redCheck(imgHSV)
	
	#hierarchy
	
	
	cv2.imshow(imgHSV)