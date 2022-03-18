#arlobox.py

# Netgear Arlo camera automation

# Monitor the momentary toggle switch in the Raspberry Pi box,
# or the armed state of an external security alarm system,
# then change the arm/disarm mode of the Arlo cameras,
# and set the lights on the box appropriately.

#Copyright (c) 2016,2022, Len Shustek 
#Open source by the MIT License; see LICENSE.txt

# 11 Aug 2015, L. Shustek, First version using mouse macros.
# 14 Sep 2016, L. Shustek, Redo using HTTP instead of mouse movement.
# 20 Sep 2016, L. Shustek, Add optional delay before arm.
# 24 Sep 2016, L. Shustek, Add input from an external security alarm system.
# 25 Jan 2022, L. Shustek, Ignore logout errs; we get "401 Unauthorized" suddenly.
# 29 Jan 2022, L. Shustek, Link to IFTTT to send an email when arm/disarm changes.
# 20 Feb 2022, L. Shustek, The new Arlo 2FA breaks Jeffrey Walter's library, so 
#                          use IFTTT instead to arm/disarm the camera

IFTTT_LOCATION = "My house"
IFTTT_KEY = "xxxxxxxxxxxxxxxxxxxxxx"  #get this from www.ifttt.com for your applet
 
import RPi.GPIO as GPIO
import time
import requests

time.sleep(15) # delay to allow other boot processes to start first
armdelay = 30  # optional delay before arming, in seconds

# Raspberry Pi's P-1 connector pin numbers for the switches and lights
upswitch = 21     # arm (momentary grounded input)
downswitch = 19   # disarm (momentary grounded input)
alarmswitch = 7   # alarm system on (grounded input)
redled = 23       # "camera armed" LED (output)
greenled = 15     # "camera disarmed" LED (output)

def sendemail(message):
   if IFTTT_KEY:
       r = requests.post('https://maker.ifttt.com/trigger/'+"email request"+"/with/key/"+IFTTT_KEY,
          params={"value1":IFTTT_LOCATION,"value2":message})
       print("IFTTT email return:", r)
     
print("configuring I/O pins...")
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(upswitch, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(downswitch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(alarmswitch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(redled, GPIO.OUT, initial=1) 
GPIO.setup(greenled, GPIO.OUT, initial=1) 
sendemail("alarm restarted")

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
       time.sleep(0.875)
       setleds(0,0)
       time.sleep(0.125)     

def do_arm():
    blinkleds(2)
    r = requests.post('https://maker.ifttt.com/trigger/'+"security arm"+"/with/key/"+IFTTT_KEY,
          params={"location":IFTTT_LOCATION,"state":"arm"})
    print("IFTTT arm trigger return:", r)
    if r.status_code == 200:
        sendemail("camera armed")
        setleds(0,1)
    else:
        errorleds(10)
 
def do_disarm():
    blinkleds(2)
    r = requests.post('https://maker.ifttt.com/trigger/'+"security disarm"+"/with/key/"+IFTTT_KEY,
          params={"location":IFTTT_LOCATION,"state":"disarm"})
    print("IFTTT disarm trigger return:", r)
    #print(vars(r))
    if r.status_code == 200:
        sendemail("camera disarmed")
        setleds(1,0)
    else:
        errorleds(10)
            
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
                if(armdelay > 0):
                    waitleds(armdelay)
                do_arm()    

#eof
