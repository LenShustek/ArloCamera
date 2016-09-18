#arlobox.py

# Monitor the switch in the Raspberry Pi box,
# change the arm/disarm mode of the Arlo camera,
# and set the lights on the box appropriately.

#Copyright (c) 2016, Len Shustek 
#Open source by the MIT License; see LICENSE.txt

USERNAME = "xxxxxxxxx"
PASSWORD = "yyyyyyyyy"

from Arlo import Arlo # from https://github.com/jeffreydwalter/arlo, as modified here
import RPi.GPIO as GPIO
import time

# Raspberry Pi P1 connector pin numbers for the switches and lights
upswitch = 21    # arm
downswitch = 19  # disarm
redled = 23      # "camera armed"
greenled = 15    # "camera disarmed"

print("configuring I/O pins...")
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(upswitch, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(downswitch, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(redled, GPIO.OUT, initial=1) 
GPIO.setup(greenled, GPIO.OUT, initial=1) 

def setleds(green,red):
    GPIO.output(greenled,green)
    GPIO.output(redled,red)

def blinkleds(times):
    for i in range(times):
        setleds(0,0)
        time.sleep(0.3)
        setleds(1,1)
        time.sleep(0.3)

def errorleds():
    for i in range(10):
        setleds(1,0)
        time.sleep(0.2)
        setleds(0,1)
        time.sleep(0.2)
        setleds(1,1)

def changemode(arm):
    try:
        arlo = Arlo(USERNAME,PASSWORD) #log in
        basestation = [device for device in arlo.GetDevices() if device['deviceType'] == 'basestation']
        print("basestation="+basestation[0]['deviceId'])
        if arm == True:
            arlo.Arm(basestation[0]['deviceId'], basestation[0]['xCloudId'])
        else:
            arlo.Disarm(basestation[0]['deviceId'], basestation[0]['xCloudId'])
        arlo.Logout()
        return True
    except Exception as e:
        print(e)
        errorleds()
        return False

blinkleds(5) # flash lights a bunch of times to show we're here

print("waiting for switch...")
while True:
    if (GPIO.input(upswitch) == 0):
        print("switch was pushed up")
        blinkleds(2)
        if (changemode(True)): # arm
            setleds(0,1)
            print("arm succeeded")
    if (GPIO.input(downswitch) == 0):
        print("switch was pushed down")
        blinkleds(2)
        if (changemode(False)): # disarm
            setleds(1,0)
            print("disarm succeeded")

   