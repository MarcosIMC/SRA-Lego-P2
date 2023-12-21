#!/usr/bin/env python3

# *=> imports
from enum import Enum
import math

from ev3dev2.button import Button

# movement (left: A, right: D)
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveSteering

# arm movement (-degrees: front, degrees: back)
from ev3dev2.motor import MediumMotor, OUTPUT_C

# color sensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_4

# touch sensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor import INPUT_3

# us sensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2

# leds
from ev3dev2.led import Leds

# oth
from time import sleep


# *=> conts

D_LEFT_WHEEL=55
D_RIGHT_WHEEL=56

D_WHEELS=125


P_LEFT_WHEEL=D_LEFT_WHEEL*math.pi
P_RIGHT_WHEEL=D_RIGHT_WHEEL*math.pi

P_WHEELS=D_WHEELS*math.pi


leds = Leds()
ts = TouchSensor(INPUT_3)
arm = MediumMotor(OUTPUT_C)
steer = MoveSteering( OUTPUT_A, OUTPUT_D)
usSensor = UltrasonicSensor(INPUT_2)
btn = Button()
colorSensor = ColorSensor(INPUT_4)


# *=> vars

# defs

# functions
def move(distance, speed=15, brake=True, block=True):

    distance*=10

    degrees= 360*distance/P_RIGHT_WHEEL

    steer.on_for_degrees(0, speed=speed, degrees=degrees, brake=brake, block=block)

def spin(degrees, spin=100, speed=15, brake=True, block=True):

    distance*=10

    degrees_left= P_WHEELS*degrees/P_LEFT_WHEEL
    degrees_right= P_WHEELS*degrees/P_RIGHT_WHEEL
    
    steer.on_for_degrees(spin, speed=speed, degrees=degrees_right, brake=brake, block=block)



#*=> main

logs = []    

leds.all_off()
leds.set_color( "LEFT","GREEN", pct=1)

while not btn.any(): pass

measure =  usSensor.distance_centimeters
while colorSensor.reflected_light_intensity < 15:
    logs.append(colorSensor.reflected_light_intensity)
    leds.set_color( "LEFT","GREEN", pct=1)
    move(10, 15, block=False)
leds.set_color( "LEFT","RED", pct=1)


    # while( measure > 10):
        
    #     if(measure > 100): continue
    #     leds.set_color('RIGHT', "RED")
    #     move(measure*.8-5, 15, False)
    #     sleep(1)
    #     measure = usSensor.distance_centimeters
    #     logs.append(measure)

    # leds.set_color("LEFT", 'AMBER')
    # if btn.any(): break

print(logs, file=open("colors.txt", "a"))