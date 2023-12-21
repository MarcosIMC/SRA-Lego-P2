#!/usr/bin/env python3

from ev3dev2.motor import MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev2.button import Button
from time import sleep

import math

# left_motor= LargeMotor(OUTPUT_B)
# right_motor = LargeMotor(OUTPUT_C)


D_LEFT_WHEEL=55
D_RIGHT_WHEEL=56

D_WHEELS=125


P_LEFT_WHEEL=D_LEFT_WHEEL*math.pi
P_RIGHT_WHEEL=D_RIGHT_WHEEL*math.pi

P_WHEELS=D_WHEELS*math.pi

# Declarations
steer = MoveSteering(OUTPUT_B, OUTPUT_C)
btn = Button()

# functions
def move(distance, speed=15):

    degrees= 360*distance/P_RIGHT_WHEEL

    steer.on_for_degrees(0, speed=speed, degrees=degrees, brake=True, block=True)

def spin(degrees, spin=100, speed=15):
    degrees_left= P_WHEELS*degrees/P_LEFT_WHEEL
    degrees_right= P_WHEELS*degrees/P_RIGHT_WHEEL
    
    steer.on_for_degrees(spin, speed=speed, degrees=degrees_right, brake=True, block=True)

# Execution
for i in range(0, 10):
    for i in range(0, 4):
        move(1000)
        sleep(.9)
        spin(90)
    while not btn.any():
        pass
    sleep(1)

for i in range(0, 10):
    for i in range(0, 4):
        move(1000)
        sleep(.9)
        spin(90, spin=-100)
    while not btn.any():
        pass
    sleep(1)