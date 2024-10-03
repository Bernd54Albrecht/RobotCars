#! /usr/bin/python3
# Code for driving a robot car with L298N
# Motors attached to GPIO 13,19,26;16,20,21
# For motor control, use Android App Bluedot by Martin O'Hanlon
# Install Python library (module) with: sudo pip3 install bluedot
# By Bernd54Albrecht

from bluedot import BlueDot
from time import sleep
from gpiozero import LED, PWMLED, Button
from subprocess import check_call
import _thread   

dot = BlueDot(auto_start_server = False)
dot.allow_pairing()
# 
# robot = Robot(left=(13,19), right=(20,16))
# motor1_enable = OutputDevice(26, initial_value=0)
# motor2_enable = OutputDevice(21, initial_value=0) 

## define 3 fragments of the 5-digit-code, idle is 16160
cy = 16     # forward/backward, digit 1 and 2
cx = 16     # left/right, digit 3 and 4
cb = 0      # button, digit 5 

# Initialisation of motors
vBatt = 7.4                # insert battery voltage
m1e = PWMLED(26)
m11 = LED(13)
m12 = LED(19)
m2e = PWMLED(12)
m21 = LED(20)
m22 = LED(16)
factor = 6/vBatt

# shutdown option iaw gpiozero docs para 2.8
def shutdown():
    check_call(['sudo', 'poweroff'])

shutdown_btn = Button(21, hold_time=2)
shutdown_btn.when_held = shutdown

def pressed(pos):
    cy = int(round(15*pos.y))
    cx = int(round(15*pos.x))
    print("pressed, y, x = ",cy,cx)
    _thread.start_new_thread(motor,(cy,cx))
  
def client_connected():
    print("connected callback")

def client_disconnected():
    print("disconnected callback")
    _thread.start_new_thread(motor,(0,0))

def getCode():
    dot.when_pressed = pressed

    dot.wait_for_press()
    print("wait for press")
    return

# self-defined function for 2 motors with PWM
def motor(cy, cx):
    if cy>=0:
        leftWheel = cy + 0.5 * cx
        rightWheel = cy - 0.5 * cx
    if cy<0:
        leftWheel = cy - 0.5 * cx
        rightWheel = cy + 0.5 * cx    
    if leftWheel > 15:
        leftWheel = 15
    if leftWheel < -15:
        leftWheel = -15
    if rightWheel > 15:
        rightWheel = 15
    if rightWheel < -15:
        rightWheel = -15
    if leftWheel < -3:
        m11.off()
        m12.on()
    elif leftWheel > 3:
        m11.on()
        m12.off()
    else:
        m11.off()
        m12.off()
    if rightWheel < -3:
        m21.off()
        m22.on()
    elif rightWheel > 3:
        m21.on()
        m22.off()
    else:
        m21.off()
        m22.off()
    m1e.value = factor * ((10 + abs(leftWheel))/32)
    print("leftWheel = ",leftWheel)    
    m2e.value = factor * ((10 + abs(rightWheel))/32)
    print("rightWheel = ",rightWheel)    

try:
    dot.start()
    dot.when_client_connects = client_connected
    dot.when_client_disconnects = client_disconnected  
    while True:
        getCode()
        sleep(0.1)
finally:
    dot.stop()
    
    

            

