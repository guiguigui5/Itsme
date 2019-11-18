import RPi.GPIO as GPIO
import sys
import os
import time
import threading

def sc_off():
    os.system('xscreensaver-command -deactivate')
    time.sleep(1)

def sc_on():
    global count
    count += 1
    time.sleep(1)

    if GPIO.input(PIR):
        count = 0
        
    if count == 5:
        os.system('xscreensaver-command -activate')
    
count = 0
PIR = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)

while True:
        
    if GPIO.input(PIR):
        sc_off()
    else:
        sc_on()
                
GPIO.cleanup()        
