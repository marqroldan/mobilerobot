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

def doTurnProcedure(turnDirection):
	print("TURNING: " + str(turnDirection))
	if turnDirection < 0:
		move_py.movement_func(1)
		time.sleep(0.4)
		move_py.movement_func(2)
	else:
		move_py.movement_func(1)
		time.sleep(0.4)
		move_py.movement_func(3)
	
	time.sleep(3)
	return


def doStopProcedure():
	print("ROBOT STOPPING")
	move_py.movement_func(1)
	time.sleep(0.4)
	move_py.movement_func(99)
	time.sleep(3)
	return


def doTurnAroundProcedure():
	print("ROBOT TURNING AROUND")
	move_py.movement_func(8)
	#time.sleep(3)
	return



Kernel_size=15
low_threshold=40
high_threshold=120

rho=10
threshold=15
theta=np.pi/180
minLineLength=100
maxLineGap=1


#For black
Hmin = 0
Hmax = 180
Smin = 0
Smax = 255
Vmin = 0
Vmax = 255

#For blue
Hmin = 100
Hmax = 140
Smin = 160
Smax = 255
Vmin = 0
Vmax = 255



rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)


#For red
Hmin = 0
Hmax = 10
Smin = 1
Smax = 255
Vmin = 0
Vmax = 255


rangeMinRed = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMaxRed = np.array([Hmax, Smax, Vmax], np.uint8)

#For red
Hmin = 170
Hmax = 180
Smin = 1
Smax = 255
Vmin = 0
Vmax = 255


rangeMinRed1 = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMaxRed1 = np.array([Hmax, Smax, Vmax], np.uint8)

minArea = 50
angle = 0

continue1 = False
#move_py.movement_func(sys.argv[1])
#VARS DEFAULT
leaving=False
returning=False
hasTurned=False
sawDotForTurn=0
sawDotForStop=0
turnedAround = False
turnDirection=0
dontDo = False
redBuff = 100
goHome = False
lastLineDirection = 0
mayNakitangRed = False

video_capture = WebcamVideoStream(src='http://127.0.0.1:8081/').start()
#video_capture = cv2.VideoCapture(-1)
#numberOfStops = -1
#definedStops = array ( 1 => array(1, 5) )
autoFile = open("autoStart.txt","w")
autoFile.write('1')
autoFile.close()
fs = False 

#Initialize camera

blank_image = np.zeros((30,100,3), np.uint8)
agi = 1
farCenterBuff = 1
lastTryAngle = 0
moveTry = 0
allTry = 0
LaneArea = 100
while True:
	
	angle = 0
	frame = video_capture.read()
	orig = imutils.resize(frame, width=400)
	frame = orig
	imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)	
	imgThresh = cv2.inRange(imgHSV, rangeMinRed, rangeMaxRed)
	imgErode = imgThresh
	
	### START LANE DETECTION
	_, contours, hierarchy = cv2.findContours(imgErode,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	areas = [cv2.contourArea(c) for c in contours]
	
	if np.any(areas):
		allTry = 1
		max_index = np.argmax(areas)
		cnt=contours[max_index]
		#centroid arx, ary
		(arx, ary), (bry, brx), rect_angle = cv2.minAreaRect(cnt)
		
		width = brx
		if(width < 60):
			continue
		height = bry
		print("arx: ", arx, " | ary : ", ary)
		print("width: ", width, " | height : ", height)
		print("rect; ", rect_angle)
		
		
		if (False):
			print("NO LANE FOUND. WIDTH > HEIGHT")
		else:
			angle = 90 - rect_angle if (width < height) else -rect_angle
			angle -= 90
			bax,bay,w,h = cv2.boundingRect(cnt)
			print("x: ", bax, " | y : ", bay)
			print("width: ", w, " | height : ", h)
			
			cv2.rectangle(frame, (int(arx), int(ary)), (int(arx+width), int(ary+height)), (0, 255, 0), 2)
			cv2.drawContours(frame, [cnt], -1, (0,255,0), 2)
	cv2.imshow("line detect test", frame)
	agi +=1
	
	if(agi>=20): 
		agi = 1
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		move_py.movement_func(99)
		pyDie(video_capture)
	

# When everything is done, release the capture




