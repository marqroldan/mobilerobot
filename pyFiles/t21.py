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
	
def delayRightWheel():
	move_py.movement_func(99)
	move_py.movement_func(10)
	time.sleep(0.03)
	move_py.movement_func(99)

def lineFix1(video_capture, lastX = -1):
	#Function kapag may nakikita pang blue pero wala sa gitna
	sleepTime = 0.3
	frame = video_capture.read()
	frame = imutils.resize(frame, width=400)
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	sawLane, laneCenterX, laneCenterY, laneWidth, laneHeight, laneAngle = laneCheck(frame)
	while sawLane and (laneCenterX <= leftLimit or laneCenterX >= rightLimit):
		lastX = laneCenterX
		frame = video_capture.read()
		frame = imutils.resize(frame, width=400)
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		sawLane, laneCenterX, laneCenterY, laneWidth, laneHeight, laneAngle = laneCheck(frame)
		if(laneCenterX < leftLimit):
			print("moveGreen naligaw to Left")
			move_py.movement_func(6)
			time.sleep(timemoveside)
			delayRightWheel()
		elif(laneCenterX > rightLimit):
			print("moveGreen naligaw to Right")
			move_py.movement_func(7)
			time.sleep(timemoveside)
			move_py.movement_func(99)
		
		time.sleep(sleepTime)
	return lastX, sawLane

def lineFix2(video_capture, sawLane, lastX = -1):
	#Function kapag walang nakikita na blue
	sleepTime = 0.3
	while sawLane == False: 
		frame = video_capture.read()
		frame = imutils.resize(frame, width=400)
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		sawLane, laneCenterX, laneCenterY, laneWidth, laneHeight, laneAngle = laneCheck(frame)
		
		if sawLane and (laneCenterX <= leftLimit or laneCenterX >= rightLimit):
			sawLane = False
			lastX = laneCenterX
			
		if(lastX < leftLimit):
			print("moveGreen naligaw to Left")
			move_py.movement_func(6)
			time.sleep(timemoveside)
			delayRightWheel()
		elif(lastX > rightLimit):
			print("moveGreen naligaw to Right")
			move_py.movement_func(7)
			time.sleep(timemoveside)
			move_py.movement_func(99)
		
		time.sleep(sleepTime)
	return lastX, sawLane

def moveGreen(video_capture):
	greenFound1 = False 
	sleepTime = 0.3
	mgLastX = -1
	while greenFound1 == False:
		move_py.movement_func(1)
		print("Greenfound:", greenFound1)
		time.sleep(moveforwardspeed)
		print("nandito move green")
		#move_py.movement_func(99)
		delayRightWheel()
		mgLastX, sawLane= lineFix1(video_capture, mgLastX)
		mgLastX, sawLane= lineFix2(video_capture, sawLane, mgLastX)
		
		frame = video_capture.read()
		frame = imutils.resize(frame, width=400)
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		centerX = -1
		centerY = -1
		width = 0
		height = 0
		rect_angle = 0
		imageGreen = cv2.inRange(frame, np.array([40, 100, 150], np.uint8), np.array([80, 255, 255], np.uint8))
		
		_, contours, hierarchy = cv2.findContours(imageGreen,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		areas = [cv2.contourArea(c) for c in contours]
		if np.any(areas):
			max_index = np.argmax(areas)
			cnt=contours[max_index]
			(centerX, centerY), (width, height), rect_angle = cv2.minAreaRect(cnt)
			print("Saw something")
			if (width * height) > 4000:
				print("yuh seen")
				greenFound1 = True
				break
				move_py.movement_func(99)
		time.sleep(sleepTime)
	
	print("Greenfound:", greenFound1)

def getPastRed(video_capture):
	frame = video_capture.read()
	frame = imutils.resize(frame, width=400)
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	sawRed, redCenterX, redCenterY, redWidth, redHeight, redAngle = redCheck(frame)
	mgLastX = -1
	while sawRed == True:
		print("Trying to get past red")
		move_py.movement_func(1)
		time.sleep(moveforwardspeed)
		#move_py.movement_func(99)
		delayRightWheel()
		frame = video_capture.read()
		frame = imutils.resize(frame, width=400)
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		sawRed, redCenterX, redCenterY, redWidth, redHeight, redAngle = redCheck(frame)
		if sawRed == False:
			break
		else:
			mgLastX, sawLane = lineFix1(video_capture, mgLastX)
			mgLastX, sawLane = lineFix2(video_capture, sawLane, mgLastX)
		time.sleep(0.3)
		
		

def doTurnProcedure(turnDirection, video_capture, findGreen = True):
	print("TURNING: " + str(turnDirection))
	if findGreen:
		moveGreen(video_capture)
	sleeptime = 0.5;
	rotatespeed = 0.11
	if turnDirection < 0:
		#left
		dflag = 6
	else:
		dflag = 7
		
	move_py.movement_func(dflag)
	time.sleep(0.15)
	move_py.movement_func(99)
	frame = video_capture.read()
	orig = imutils.resize(frame, width=400)
	frame = orig
	imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	sawLane, laneCenterX, laneCenterY, laneWidth, laneHeight, laneAngle = laneCheck(imgHSV)
	
	if turnDirection < 0:
		lgCheck = laneCenterX < 200
	else:
		lgCheck = laneCenterX > 200
		
	while(sawLane and lgCheck):
		checkAutoFile = open("masterOff.txt","r")
		if(checkAutoFile.read(1)=='0'):
			move_py.movement_func(99)
			checkAutoFile.close()
			pyDie(video_capture)
			
		checkAutoFile = open("masterOff.txt","r")
		if(checkAutoFile.read(1)=='2'):
			move_py.movement_func(99)
			checkAutoFile.close()
			continue
		
		checkAutoFile.close()
			
		if(move_py.readRoboAutoStop()): 
			move_py.turnoffALlPins()
			pyDie(video_capture)
		print('second pass')
		move_py.movement_func(dflag)
		time.sleep(rotatespeed)
		move_py.movement_func(99)
		frame = video_capture.read()
		orig = imutils.resize(frame, width=400)
		frame = orig
		imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		sawLane, laneCenterX, laneCenterY, laneWidth, laneHeight, laneAngle = laneCheck(imgHSV)
		if turnDirection < 0:
			lgCheck = laneCenterX < 200
		else:
			lgCheck = laneCenterX > 200
		time.sleep(sleeptime)
	lgCheck = True
	while(sawLane==False or lgCheck):
		print('third pass')
		move_py.movement_func(dflag)
		time.sleep(rotatespeed)
		move_py.movement_func(99)
		frame = video_capture.read()
		orig = imutils.resize(frame, width=400)
		frame = orig
		imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		sawLane, laneCenterX, laneCenterY, laneWidth, laneHeight, laneAngle = laneCheck(imgHSV)
		lgCheck = laneCenterX < leftLimit or laneCenterX > rightLimit
		time.sleep(sleeptime)
		print("sawLane: ", sawLane, "lgCheck: ", lgCheck, "laneCenter: ", laneCenterX)
		#cv2.imshow("line detect test1", frame)
		
		
	#time.sleep(9999)
	return 


def doStopProcedure():
	print("ROBOT STOPPING")
	move_py.movement_func(1)
	time.sleep(0.8)
	delayRightWheel()
	time.sleep(3)
	return


def doTurnAroundProcedure(video_capture):
	print("ROBOT TURNING AROUND")
	move_py.movement_func(1)
	time.sleep(0.15)
	delayRightWheel()
	move_py.movement_func(8)
	doTurnProcedure(turnDirection, video_capture, False)
	#time.sleep(3)
	return

def redCheck(frame):
	centerX = -1
	centerY = -1
	width = 0
	height = 0
	rect_angle = 0
	
	imgThreshRed = cv2.inRange(imgHSV, np.array([0, 1, 0], np.uint8), np.array([10, 255, 255], np.uint8))
	_,contoursRed, hierarchyRed = cv2.findContours(imgThreshRed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	areasRed = [cv2.contourArea(c) for c in contoursRed]
	
	foundRed = False
	if np.any(areasRed):
		max_index = np.argmax(areasRed)
		cnt=contoursRed[max_index]
		(centerX_t, centerY_t), (width_t, height_t), rect_angle_t = cv2.minAreaRect(cnt)
		if (width_t * height_t) > 3000:
			foundRed = True
			height = height_t 
			width = width_t
			centerY = centerY_t
			centerX = centerX_t
			rect_angle = rect_angle_t
	return (foundRed, centerX, centerY, width, height, rect_angle)

def laneCheck(frame):
	centerX = -1
	centerY = -1
	width = 0
	height = 0
	rect_angle = 0
	imgLane = cv2.inRange(frame, np.array([100, 160, 0], np.uint8), np.array([140, 255, 255], np.uint8))
	_, contours, hierarchy = cv2.findContours(imgLane,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	areas = [cv2.contourArea(c) for c in contours]
	foundLane = False
	if np.any(areas):
		allTry = 1
		max_index = np.argmax(areas)
		cnt=contours[max_index]
		(centerX_t, centerY_t), (width_t, height_t), rect_angle_t = cv2.minAreaRect(cnt)
		if (width_t * height_t) > 3000:
			foundLane = True
			height = height_t 
			width = width_t
			centerY = centerY_t
			centerX = centerX_t
			rect_angle = rect_angle_t
	return (foundLane, centerX, centerY, width, height, rect_angle)


Kernel_size=15
low_threshold=40
high_threshold=120

rho=10
threshold=15
theta=np.pi/180
minLineLength=100
maxLineGap=1

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
adjuster = 0
leftLimit = 170 - adjuster
rightLimit = 230 + adjuster

video_capture = WebcamVideoStream(src='http://127.0.0.1:8081/').start()
print(sys.argv[1])
if len(sys.argv) > 1:
	definedStops = json.loads(sys.argv[1])
	numberOfStops = int(sys.argv[2])
	if numberOfStops == 0:
		print("Not enough parameters given. Exiting")
		pyDie(video_capture)
else:
	print("Not enough parameters given. Exiting")
	pyDie(video_capture)

autoFile = open("masterOff.txt","w")
autoFile.write('1')
autoFile.close()
fs = False 

#Initialize camera

agi = 1
farCenterBuff = 1
lastTryAngle = 0
moveTry = 0
allTry = 0
nTry = 0
LaneArea = 100
trying=False
calibrated=True
difference = 30
timefrontleft = 0.07
timefrontright = 0.07
#timefrontleft = 0.1
#timefrontright = 0.1
timemoveside = 0.07
moveforwardspeed = 0.13
wrongdotmoveforward = 0.1
iikotsiyapakaunti = 0.2
firstikotpakaliwa = 0.73

move_py.movement_func(12345)
ccount = 0


while True:
	angle = 0
	minRedHeight = 80
	frame = video_capture.read()
	orig = imutils.resize(frame, width=400)
	frame = orig
	imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	checkAutoFile = open("masterOff.txt","r")
	if(checkAutoFile.read(1)=='0'):
		move_py.movement_func(99)
		checkAutoFile.close()
		pyDie(video_capture)
		
	checkAutoFile = open("masterOff.txt","r")
	if(checkAutoFile.read(1)=='2'):
		move_py.movement_func(99)
		checkAutoFile.close()
		continue
	
	checkAutoFile.close()
		
	if(move_py.readRoboAutoStop()): 
		move_py.turnoffALlPins()
		pyDie(video_capture)
	
	if returning==True:
		if turnedAround==False:
			#pass
			turnedAround = True
			doTurnAroundProcedure(video_capture)
		
		if sawDotForStop > 0:
			print("SAW RED AGAIN, IMMA SUBTRACT")
			sawDotForStop-=1
			#redBuff =  50
			print("sawDotForStop:"+str(sawDotForStop))
		
		else:
			z = 1
	else:
		pass
	
	#imgThreshRed = cv2.inRange(imgHSV, rangeMinRed, rangeMaxRed)
	#imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
	#imgErode = imgThresh
	
	### RED DETECTION
	#_,contoursRed, hierarchyRed = cv2.findContours(imgThreshRed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#areasRed = [cv2.contourArea(c) for c in contoursRed]
	
	redBuff+=1
	
	sawRed, redCenterX, redCenterY, redWidth, redHeight, redAngle = redCheck(imgHSV)
	
	if (sawRed): #if np.any(areasRed):
		#time.sleep(99)
		if redWidth > 60 and redCenterY > 90:
			#may nakita siyang dot
			if redBuff > 100:
				#check kung nasa gitna ba ng screen yung red
				if(False):#redCenterY < 130):
					print("May nakitang red kaso malayo sa vertical center")
					mayNakitangRed = False
				else:
					redBuff = 1
					mayNakitangRed = True
					print("Nakakita nanaman ako within spec")
					#move_py.movement_func(1)
					#time.sleep(0.1*(minRedHeight / (difference)))
					#move_py.movement_func(99)
					if numberOfStops==0 and goHome:
						#move_py.movement_func(1)
						#time.sleep(0.1)
						#delayRightWheel()
						#print("DTP MAY NAKITA")
						#doTurnProcedure(1,video_capture)
						#frame = video_capture.read()
						#orig = imutils.resize(frame, width=400)
						#frame = orig
						#imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
						#sawRed, redCenterX, redCenterY, redWidth, redHeight, redAngle = redCheck(imgHSV)
						#while sawRed==False:
						#	frame = video_capture.read()
						#	orig = imutils.resize(frame, width=400)
						#	frame = orig
						#	imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
						#	sawRed, redCenterX, redCenterY, redWidth, redHeight, redAngle = redCheck(imgHSV)
						#	move_py.movement_func(1)
						#	time.sleep(moveforwardspeed)
						#	delayRightWheel()
						pyDie(video_capture)
			else:
				#print("Kulang pa sa buff")
				mayNakitangRed = False
				pass
				#print("redBuff:"+str(redBuff))
		else:
			pass
			#print("May nakita ako kaso wala sa spec na 700")
	### END BLOB DETECTION
	
	### START LANE DETECTION
	
	sawLane, laneCenterX, laneCenterY, laneWidth, laneHeight, laneAngle = laneCheck(imgHSV)
	
	#if(laneWidth > 150):
		#move_py.movement_func(1)
		#time.sleep(moveforwardspeed)
		#move_py.movement_func(99)
		#sawLane = False
	
	if sawLane: #np.any(areas):
		allTry = 1
		if (False):
			print("NO LANE FOUND. WIDTH > HEIGHT")
		else:
			#angle = 90 - rect_angle if (width < height) else -rect_angle
			#angle -= 90
			#bax,bay,w,h = cv2.boundingRect(cnt)
			#print('w',w)
			#print('h',h)
			#print('width',width)
			#print('height',height)
			if (False):#if w >= 600:
				print("Please place your hand in front of the camera momentarily.")
				move_py.movement_func(99)
				continue
			
			if (laneHeight * laneWidth) > 3000:
				if(returning==True and turnedAround==False and trying==True):
					turnedAround = True
					trying = False
				elif(returning==True and turnedAround==False and trying==False):
					trying=True
					move_py.movement_func(6)
					time.sleep(firstikotpakaliwa)
					delayRightWheel()
				## DIRECTION CHECKER 1
				farCenterBuff +=1
				#print("farCenter:"+str(farCenterBuff))
				#IF LANE IS OUT OF BOUNDS
				#print("line centroid: "+str(laneCenterX))
				if (laneCenterX <= rightLimit and laneCenterX >= leftLimit)==False and farCenterBuff > 15:
					print("out of bounds na siya")
					farCenterBuff = 1
					fs = False
					#if (laneCenterX - 320) > 0:
					if(laneCenterY < 130):
						move_py.movement_func(1)
						time.sleep(timemoveside)
						delayRightWheel()
					elif(laneCenterY > leftLimit):
						move_py.movement_func(4)
						time.sleep(timemoveside)
						move_py.movement_func(99)
					else:
						move_py.movement_func(1)
						time.sleep(timemoveside)
						delayRightWheel()
						
					if laneCenterX < leftLimit:
						m=1
						lastLineDirection = 1 
						print("nasa pinaka kaliwa")
						move_py.movement_func(6)
						time.sleep(timefrontright)
						delayRightWheel()
						#time.sleep(0.5)
					elif laneCenterX > rightLimit:
						m=1
						lastLineDirection = -1 
						print("nasa pinaka kanan")
						move_py.movement_func(7)
						time.sleep(timefrontleft)
						move_py.movement_func(99)
						#time.sleep(0.5)
				else:
					#farCenterBuff = 1
					#print("wala sa limit")
					#if laneCenterX < 150:
					#	m=1
					#	lastLineDirection = 1 
					#	print("more than 280")
					#	move_py.movement_func(6)
					#	time.sleep(timefrontright)
					#	move_py.movement_func(99)
					#
					#elif laneCenterX < 250:
					#	m=1
					#	lastLineDirection = -1 
					#	print("less than 120")
					#	move_py.movement_func(7)
					#	time.sleep(timefrontleft)
					#	move_py.movement_func(99)
					fs = True
					##move_py.movement_func(1) #goforward
					pass
				
				if mayNakitangRed == True:
					mayNakitangRed = False
					# RED DETECTION SIMULTANEOUS CHECK
					if returning==False:
						if hasTurned == False:
							#DIRECTION CHECKER 1
							print ("ME STILL HERE")
							sawDotForTurn+=1
							if str(sawDotForTurn) in definedStops:
								hasTurned = True
								print("Yes, papasok siya sa row na to")
								sawDotForStop = 0 #reset every row
								if redCenterX < laneCenterX:
									print("Turn Left:"+str(redCenterX))
									turnDirection=-1
									lastLineDirection=-1
									doTurnProcedure(-1, video_capture)
								else:
									print("Turn Right:"+str(redCenterX))
									turnDirection=1
									lastLineDirection=1
									doTurnProcedure(1, video_capture)
									
								ccount = len(definedStops[str(sawDotForTurn)])
								print("Count:", ccount)
							else:
								move_py.movement_func(1)
								time.sleep(wrongdotmoveforward)
								delayRightWheel()
								print("Nope, hindi siya para dito: "+str(sawDotForTurn))
								moveGreen(video_capture)
								#getPastRed(video_capture)
						else:
							if(numberOfStops > 0):
								sawDotForStop+=1
							
							print("SawDotForStop:" + str(sawDotForStop))
							try:
								if str(sawDotForStop) in definedStops[str(sawDotForTurn)]:
									#doStopProcedure()
									ccount -= 1
									print("ROBOT STOPPING")
									#move_py.movement_func(1)
									#time.sleep(0.8)
									#move_py.movement_func(99)
									#time.sleep(3)
									print("POTA OO PARA DITO SIYA")
									numberOfStops = numberOfStops - 1
									#dito yung nakakita ng stopa
									#time.sleep(5)
									if False:
										moveGreen(video_capture)
										move_py.AutoPinGo()
										while (move_py.ResponsePinStop()==False):
											print("oo false parin");
											pass
										move_py.AutoPinStop()
										time.sleep(1)
										print("hala hindi na false")
									else:
										moveGreen(video_capture)
										time.sleep(5)
										#move_py.movement_func(6)
										#time.sleep(0.1 * 3)
									
									frame = video_capture.read()
									if ccount < 1:
										returning = True
										trying=False
								else: 
									moveGreen(video_capture)
							except:
								sawDotForStop = sawDotForStop - 1
					else:
						print("Returning is set to true")
						if numberOfStops > 0:
							print("Meron pang stops na pupuntahan")
							returning = False
							turnedAround = False
							hasTurned = False
							doTurnProcedure(turnDirection, video_capture)
						else:
							#since 0 na yung numberOfStops, meaning wala na siyang pupuntahan. Dapat di na niya to pupuntahan ulit
							if goHome == False:
								goHome = True
								print("Pauwi na ako hehe")
								doTurnProcedure(turnDirection * -1, video_capture)
					
					#cv2.drawContours(frame, [cnt], -1, (0,255,0), 2)
					#cv2.circle(frame, (int(redCenterX),int(redCenterY)), 7, (255,255,255), -1)
				
				#cv2.drawContours(frame, [cnt], -1, (0,255,0), 2)
				#cv2.circle(frame, (int(laneCenterX),int(laneCenterY)), 7, (255,255,255), -1)
			else:
				print("Pumasok dito")
				
				frame = video_capture.read()
				orig = imutils.resize(frame, width=400)
				frame = orig
				imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
				sawLane, laneCenterX, laneCenterY, laneWidth, laneHeight, laneAngle = laneCheck(imgHSV)
				
				
				#while True:
				#	print("X:",laneCenterX, " Y: ", laneCenterY)
				#	move_py.movement_func(99)
				#	time.sleep(999)
				
				if(laneCenterX < leftLimit):
					print("DTP: PUmASOK NALIGAW")
					doTurnProcedure(-1, video_capture, False)
				elif(laneCenterX > rightLimit):
					print("DTP: PUmASOK NALIGAW")
					doTurnProcedure(1, video_capture, False)
				else:
					move_py.movement_func(4)
					time.sleep(0.1)
					move_py.movement_func(99)
					#doTurnProcedure(1, video_capture)
				
				#if(lastLineDirection < 0):
				#	move_py.movement_func(6)
				#	lastLineDirection=1
				#	time.sleep(timemoveside)
				#	if(ntry>5):
				#		move_py.movement_func(4)
				#		lastLineDirection=1
				#		time.sleep(0.4)
				#		move_py.movement_func(99)
				#		ntry=0
				#	move_py.movement_func(99)
				#elif(lastLineDirection > 0):
				#	move_py.movement_func(7)
				#	time.sleep(timemoveside)
				#	lastLineDirection=-1
				#	ntry+=1
				#	if(ntry>5):
				#		move_py.movement_func(4)
				#		lastLineDirection=1
				#		time.sleep(0.4)
				#		move_py.movement_func(99)
				#		ntry=0
				#	move_py.movement_func(99)
				if(returning==True and turnedAround==False):
					print('nah')
					move_py.movement_func(6)
					time.sleep(iikotsiyapakaunti)
					delayRightWheel()
				
				#ntry+=1
				#if(ntry>5):
				#	move_py.movement_func(4)
				#	time.sleep(0.4)
				#	move_py.movement_func(99)
				#	ntry=0
	else:
		#print("STOPPING. NO LANE FOUND.")	
		#print("Trying to find lane")
		print('returning',str(returning))
		print('turnedAround',str(turnedAround))
		if(returning==True and turnedAround==False):
			print("No lane found")
			trying=True
			move_py.movement_func(6)
			print('pero dito pumasok hehe')
			time.sleep(iikotsiyapakaunti)
			delayRightWheel()
		else:
			moveTry +=1
			allTry +=1
			if allTry < 30:
				if(lastLineDirection > 0):
					move_py.movement_func(6)
					lastLineDirection=1
					time.sleep(timemoveside)
					delayRightWheel()
				elif(lastLineDirection < 0):
					move_py.movement_func(7)
					time.sleep(timemoveside)
					lastLineDirection=-1
					move_py.movement_func(99)
				else:
					#do backwards
					move_py.movement_func(4)
					time.sleep(timemoveside)
					move_py.movement_func(99)
					if moveTry > 10:
						moveTry = 1
						lastLineDirection = -1
					
				if moveTry > 20:
					moveTry = -23
					lastLineDirection *= -1
			
		
		time.sleep(0.2);
		fs = False 
		move_py.movement_func(99)
	
	#print("hi: "+str(fs))
	#Draw cicrcles in the center of the picture
	cv2.circle(orig,(200,150),20,(0,0,255),1)
	cv2.circle(orig,(200,150),10,(0,255,0),1)
	cv2.circle(orig,(200,150),2,(255,0,0),2)
	
	#orig[260:480, 0:640] = frame
	frame = orig
	
	#### DIRECTION CHECKER 2
	#### CHECKING BASED ON ANGLE
	if laneWidth > 120:
		lastTryAngle +=1
		if abs(angle) >= 5 and lastTryAngle > 20:
			print('angle checker')
			lastTryAngle = 1
			if angle > 0:
				cv2.putText(frame,'GO FRONT RIGHT ',(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
				lastLineDirection = 1 
				move_py.movement_func(6)
				time.sleep(timefrontright)
				delayRightWheel()
				continue
			
			else:
				cv2.putText(frame,'GO FRONT LEFT ',(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
				lastLineDirection = -1 
				move_py.movement_func(7)
				time.sleep(timefrontleft)
				move_py.movement_func(99)
				continue
		else:
			if fs == True:
				if agi > 15:
					move_py.movement_func(1)
					time.sleep(moveforwardspeed)
					delayRightWheel()
					agi = 1
	else:
		print("Dito ata pumasok")
		move_py.movement_func(1)
		time.sleep(moveforwardspeed)
		delayRightWheel()
		
	agi +=1
	
	if(agi>=20): 
		agi = 1
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		move_py.movement_func(99)
		pyDie(video_capture)
		
	cv2.imshow("line detect test", frame)
	

# When everything is done, release the capture




