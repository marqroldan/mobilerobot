import wiringpi
import time
import sys

'''SETUP wiringPi for Modification'''
wiringpi.wiringPiSetup()
wiringpi.pinMode(0,1)
wiringpi.pinMode(1,1)
wiringpi.pinMode(2,1)
wiringpi.pinMode(3,1)

wiringpi.pinMode(4,1) #output
wiringpi.pinMode(5,0) #input
roboStop_s = False

file2 = open("roboStop.txt","w")
file2.write("false")
	
file2 = open("masterFile.txt","w")
file2.write("false")

def movDie():
	file2 = open("roboStop.txt","w")
	file2.write("false")
#	sys.exit()
	return
	
def turnOffPins():
	#print("WPI: STOPPING ALL PINS")
	wiringpi.digitalWrite(0,0);
	wiringpi.digitalWrite(1,0);
	wiringpi.digitalWrite(2,0);
	wiringpi.digitalWrite(3,0);
	return

def moveForward():
	turnOffPins()
	if(readRoboStop()==False):
		print("WPI: Moving Forward")
		wiringpi.digitalWrite(0, 1)
		readRoboStop()
		wiringpi.digitalWrite(2, 1)
		readRoboStop()
	return

def moveBackward():
	turnOffPins()
	if(readRoboStop()==False):
		print("WPI: Moving Backward")
		wiringpi.digitalWrite(1, 1)
		readRoboStop()
		wiringpi.digitalWrite(3, 1)
		readRoboStop()
	return

def rotateRight():
	turnOffPins()
	if(readRoboStop()==False):
		print("WPI: Rotating Right")
		wiringpi.digitalWrite(0, 1)
		readRoboStop()
		wiringpi.digitalWrite(3, 1)
		readRoboStop()
	return

def rotateLeft():
	turnOffPins()
	if(readRoboStop()==False):
		print("WPI: Rotating Left")
		wiringpi.digitalWrite(1, 1)
		readRoboStop()
		wiringpi.digitalWrite(2, 1)
		readRoboStop()
	return
	
def readRoboStop():
	file = open("roboStop.txt","r")
	line = list(file.readlines())
	line=line[0].splitlines()[0]
	if(line=="true"):
		print("yeah")
		turnOffPins()
		movDie()
		return True
	else:
		return False
	
def readRoboAutoStop():
	file = open("roboStop.txt","r")
	line = list(file.readlines())
	line=line[0].splitlines()[0]
	if(line=="true"):
		print("yeah")
		turnOffPins()
		movDie()
		return True
	else:
		return False

def AutoPinGo():
	wiringpi.digitalWrite(4,1)
	return

def ResponsePinStop():
	if wiringpi.digitalRead(5)==1:
		wiringpi.digitalWrite(4,0)
		return True
	else:
		return False
		
def AutoPinStop():
	wiringpi.digitalWrite(4,0)
	return


def movement_func(arg1):
	moveforwardtime = 0.8
	moveside = 0.4
	readRoboAutoStop()
	
	arg1 = int(arg1)
	if arg1==1:
		#forward
		moveForward()
	elif arg1==2:
		#left
		#moveForward()
		#time.sleep(moveforwardtime)
		rotateLeft()
		time.sleep(moveside)
		turnOffPins()
	elif arg1==3:
		#right
		rotateRight()
		time.sleep(moveside)
		turnOffPins()
	elif arg1==4:
		#reverse
		moveBackward()
	elif arg1==5:
		#stop
		turnOffPins()
	elif arg1==6:
		#rotateLeft
		rotateLeft()
	elif arg1==7:
		#rotateRight
		rotateRight()
	elif arg1==8:
		#360CounterClockwise
		print("WPI: 360: CounterClockwise")
		rotateLeft()
		time.sleep(0.8)
		turnOffPins()
	elif arg1==9:
		#360Clockwise
		print("WPI: 360: Clockwise")
		moveForward()
		time.sleep(0.6)
		rotateRight()
		time.sleep(1.2)
		turnOffPins()
	else:
		turnOffPins()
		
	return

if __name__ == "__main__":
    movement_func(sys.argv[1])
