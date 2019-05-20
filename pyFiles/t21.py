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

def initialize_robo():
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

def fixLane(centerX, centerY, video_capture):
	if centerX <= 170 or centerX >= 230):
		#Stop All Movement
		move_py.movement_func(99)
		outOfLane = True
		
		while outOfLane == True:
			if centerX <= 170:
				#move to left
				move_py.movement_func(6)
			elif centerX >= 230:
				#move to right
				move_py.movement_func(6)
				
			frame = video_capture.read()
			orig = imutils.resize(frame, width=400)
			frame = orig
			difference = 0
			imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
			foundLane, centerX_LANE, centerY_LANE, width_LANE, height_LANE, rect_angle_LANE = laneCheck(imgHSV)
			if centerX_LANE <= 230 and centerX_LANE >= 170:
				#turn Off Movement
				move_py.movement_func(99)
				outOfLane = False
				
	return frame

def moveForwardFindGreen(video_capture):
	greenFound = False 
	
	while greenFound == False:
		frame = video_capture.read()
		orig = imutils.resize(frame, width=400)
		frame = orig
		difference = 0
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		foundLane, centerX_LANE, centerY_LANE, width_LANE, height_LANE, rect_angle_LANE = laneCheck(frame)
		if foundLane:
			frame = fixLane(centerX_LANE, centerY_LANE, video_capture)
		
		#::FOR GREEN (H, S, V)
		rangeMin = np.array([60, 100, 50], np.uint8)
		rangeMax = np.array([60, 255, 255], np.uint8)
		centerX = -1
		centerY = -1
		width = 0
		height = 0
		rect_angle = 0
		imgThresh = cv2.inRange(frame, rangeMin, rangeMax)
	
		_, contours, hierarchy = cv2.findContours(imgThresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		areas = [cv2.contourArea(c) for c in contours]
		if np.any(areas):
			foundLane = True
			allTry = 1
			max_index = np.argmax(areas)
			cnt=contours[max_index]
			(centerX, centerY), (width, height), rect_angle = cv2.minAreaRect(cnt)
			#dimension condition here
			greenFound = True
			move_py.movement_func(99)
	
	return (frame, foundLane)

def turnBasedOnDirection(video_capture, direction, green = False):
	if green == True:
		frame, foundLane = moveForwardFindGreen(video_capture)
	else:
		frame = video_capture.read()
		orig = imutils.resize(frame, width=400)
		frame = orig
		difference = 0
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		foundLane, centerX_LANE, centerY_LANE, width_LANE, height_LANE, rect_angle_LANE = laneCheck(frame)
	
	flip = False
	while foundLane == True:
		if (direction < 0):
			move_py.movement_func(6)
		else:
			move_py.movement_func(7)
		frame = video_capture.read()
		orig = imutils.resize(frame, width=400)
		frame = orig
		difference = 0
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		foundLane, centerX_LANE, centerY_LANE, width_LANE, height_LANE, rect_angle_LANE = laneCheck(frame)
		if foundLane == False:
			flip = True
			foundLane = True
		elif foundLane == True and flip == True:
			break
			
	return frame

def checkDot(video_capture, centerX_LANE, centerX_RED):
	#frame, inLane, currentRow, currentDot, numberOfStopsForRow, returning, foundRed 
	cd_frame = frame
	cd_inLane = inLane
	cd_currentRow = currentRow
	cd_currentDot = currentDot
	cd_numberOfStopsForRow = numberOfStopsForRow
	cd_returning = returning
	cd_foundRed = foundRed
	cd_lastDirection = lastDirection
	cd_numberOfStops = numberOfStops
	# < 0 left | > 0 right
		
	if goingHome == True:
		cd_currentRow = currentRow - 1
		if cd_currentRow < 1:
			moveForwardFindGreen(video_capture)
	else:
		if (centerX_RED < centerX_LANE):
			cd_lastDirection = -1
		else:
			cd_lastDirection = 1
		if inLane == True:
			if returning == True:
				cd_currentDot = currentDot - 1
				
				if currentDot < 1 and numberOfStops > 1:
					#go to the next row
					cd_frame = turnBasedOnDirection(video_capture, cd_lastDirection * -1, True);
					cd_inLane = False
				elif currentDot < 1 and numberOfStops < 1:
					cd_frame = turnBasedOnDirection(video_capture, cd_lastDirection, True);
					cd_inLane = False
					goingHome = True
					
			else:
				cd_currentDot = currentDot + 1
				
				if (str(cd_currentDot) in definedStops[str(currentRow)]):
					cd_numberOfStopsForRow = numberOfStopsForRow - 1
					cd_numberOfStops = numberOfStops - 1
					move_py.movement_func(99)
					moveForwardFindGreen(video_capture)
					#do robot procedure
					print("Doing robot procedure")
					time.sleep(5)
				
				if (numberOfStopsForRow < 1):
					cd_returning = True
					turnBasedOnDirection(video_capture, lastDirection)
		else:
			cd_currentRow = currentRow + 1
			if str(cd_currentRow) in definedStops:
				cd_frame = turnBasedOnDirection(video_capture, cd_lastDirection, True);
				cd_inLane = True
				cd_numberOfStopsForRow = count(definedStops[str(cd_currentRow)])
				cd_currentDot = 0
			else:
				moveForwardFindGreen(video_capture)
			
	return (cd_frame, cd_inLane, cd_currentRow, cd_currentDot, cd_numberOfStopsForRow, cd_returning, cd_foundRed, cd_lastDirection, cd_numberOfStops)

####### VARIABLES #########
Kernel_size=15
low_threshold=40
high_threshold=120

rho=10
threshold=15
theta=np.pi/180
minLineLength=100
maxLineGap=1

initialize_robo()

#	- arguments
#	-- Total Number of Stops 
#	-- Stops per Rows
#	- sawTrueRed
#	- sawLane
#	- masterOff
#	- movementOverride
lastDirection = 0
inLane = False
currentRow = 0
currentDot = 0
numberOfStopsForRow = 0
returning = False
goingHome = False

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
	
	foundLane, centerX_LANE, centerY_LANE, width_LANE, height_LANE, rect_angle_LANE = laneCheck(imgHSV)
	foundRed, centerX_RED, centerY_RED, width_RED, height_RED, rect_angle_RED = redCheck(imgHSV)
	
	if foundLane:
		if foundRed:
			move_py.movement_func(99)
			frame, inLane, currentRow, currentDot, numberOfStopsForRow, returning, foundRed = checkDot(video_capture)
		
		frame = fixLane(centerX_LANE, centerY_LANE, video_capture)
		
	if foundRed:
		move_py.movement_func(99)
		frame, inLane, currentRow, currentDot, numberOfStopsForRow, returning, foundRed, lastDirection, numberOfStops = checkDot(video_capture, centerX_LANE, centerX_RED)
		frame = fixLane(centerX_LANE, centerY_LANE, video_capture)
	
	move_py.movement_func(1)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		move_py.movement_func(99)
		pyDie(video_capture)
		
	cv2.imshow(imgHSV)