#arlobox.py

# Netgear Arlo camera automation

# Monitor the momentary toggle switch in the Raspberry Pi box,
# or the armed state of an external security alarm system,
# then change the arm/disarm mode of the Arlo cameras,
# and set the lights on the box appropriately.

#Copyright (c) 2016, Len Shustek 
#Open source by the MIT License; see LICENSE.txt

# 11 Aug 2015, L. Shustek, first version
# 14 Sep 2016, L. Shustek, redo using HTTP instead of mouse movement
# 20 Sep 2016, L. Shustek, Add optional delay before arm
# 24 Sep 2016, L. Shustek, Add input from an external security alarm system

USERNAME = "xxxxxxxxx"
PASSWORD = "yyyyyyyyy"

from Arlo import Arlo # from https://github.com/jeffreydwalter/arlo, as modified here
import RPi.GPIO as GPIO
import time

armdelay = 30  # optional delay before arming, in seconds

# Raspberry Pi's P-1 connector pin numbers for the switches and lights
upswitch = 21     # arm (momentary grounded input)
downswitch = 19   # disarm (momentary grounded input)
alarmswitch = 7   # alarm system on (grounded input)
redled = 23       # "camera armed" LED (output)
greenled = 15     # "camera disarmed" LED (output)

print("configuring I/O pins...")
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(upswitch, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(downswitch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(alarmswitch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(redled, GPIO.OUT, initial=1) 
GPIO.setup(greenled, GPIO.OUT, initial=1) 

def setleds(green,red):
    GPIO.output(greenled,green)
    GPIO.output(redled,red)

def blinkleds(times):
    for i in range(times):
        setleds(0,0)
        time.sleep(0.33)
        setleds(1,1)
        time.sleep(0.33)

def errorleds(times):
    for i in range(times):
        setleds(1,0)
        time.sleep(0.2)
        setleds(0,1)
        time.sleep(0.2)
    setleds(0,0)

def waitleds(times):
   for i in range(times):
       setleds(1,1)   
       time.sleep(0.25)
       setleds(1,0)
       time.sleep(0.25)
       setleds(1,1)
       time.sleep(0.25)
       setleds(0,1)
       time.sleep(0.25)
       
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
        errorleds(10)
        return False

def do_arm():
    if (armdelay > 0):
            waitleds(armdelay)
    blinkleds(2)
    if (changemode(True)): # arm
        setleds(0,1)
        print("arm succeeded")

def do_disarm():
    blinkleds(2)
    if (changemode(False)): # disarm
        setleds(1,0)
        print("disarm succeeded")

            
alarm_off = GPIO.input(alarmswitch) #current state of alarm system
blinkleds(5) # flash lights a bunch of times to show we're here

print("waiting for switch or alarm system...")
while True:
    
    if (GPIO.input(upswitch) == 0):
        print("switch was pushed up")
        do_arm()
        
    if (GPIO.input(downswitch) == 0):
        print("switch was pushed down")
        do_disarm()
        
    if (GPIO.input(alarmswitch) != alarm_off): # alarm system state change?
        time.sleep(0.5) # debounce time
        if (GPIO.input(alarmswitch) != alarm_off):
            alarm_off = GPIO.input(alarmswitch)
            if (alarm_off):
                print("alarm system was disarmed")
                do_disarm()
            else:
                print("alarm system was armed")
                do_arm()    

#eof
