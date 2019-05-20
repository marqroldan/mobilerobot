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
import multiprocessing as mp

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

#video_capture = cv2.VideoCapture(-1)
#numberOfStops = -1
#definedStops = array ( 1 => array(1, 5) )
#Initialize camera

def puc():
	video_capture = WebcamVideoStream(src='http://127.0.0.1:8081/').start()
	while True:
		
		angle = 0
		frame = video_capture.read()
		orig = imutils.resize(frame, width=200)
		frame = orig
		imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)	
		imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
		imgErode = imgThresh
		
		cv2.imshow("line detect test", frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			move_py.movement_func(99)
			pyDie(video_capture)
		
if __name__ == '__main__':
    processes = [mp.Process(target=puc, args=())]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

# When everything is done, release the capture




