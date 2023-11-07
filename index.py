#!/usr/bin/env python3

# *=> imports
from ev3dev2.motor import MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev2.button import Button
from time import sleep

import math

# *=> constants

# diameters
D_LEFT_WHEEL=55
D_RIGHT_WHEEL=56
D_WHEELS=125

# perimeters
P_LEFT_WHEEL=D_LEFT_WHEEL*math.pi
P_RIGHT_WHEEL=D_RIGHT_WHEEL*math.pi
P_WHEELS=D_WHEELS*math.pi

# progressive movement
PM_INCREMENT=5          # velocity increment every step
PM_DISTANCE=5           # distance every step

# progressive spin
PS_INCREMENT=1          # velocity increment every step
PS_DISTANCE=1           # distance every step

# *=> Declarations
btn = Button()
steer = MoveSteering(OUTPUT_B, OUTPUT_C)

# *=> functions
def basic_move(distance, speed=30, stop=False):

    degrees= 360*distance/P_RIGHT_WHEEL

    steer.on_for_degrees(0, speed=speed, degrees=degrees, brake=stop, block=not stop)

def basic_spin(degrees, spin=100, speed=15, stop=False):
    
    degrees_left= P_WHEELS*360/(P_LEFT_WHEEL*4)
    degrees_right= P_WHEELS*360/(P_RIGHT_WHEEL*4)
    
    steer.on_for_degrees(spin, speed=speed, degrees=degrees_right, brake=stop, block=not stop)


def move(distance, speed=50):
    # Para distancias variables necesitamos otro algoritmo que ajuste distancias menores a 2 veces PM_DISTANCE

    actual_speed=0
    steps = int(speed/PM_INCREMENT)
    distance -= 2*steps*PM_DISTANCE

    for i in range(0, steps):

        if(actual_speed < speed):
            actual_speed+= PM_INCREMENT

        basic_move(PM_DISTANCE, speed=actual_speed)
    
    basic_move(distance, speed=speed)

    for i in range(0, steps):
        
        basic_move(PM_DISTANCE, speed=actual_speed, stop=False if i < steps-1 else True)

        if(actual_speed > 0):
            actual_speed-= PM_INCREMENT


def spin(degrees, spin=100, speed=15):

    actual_speed=0
    steps = int(speed/PS_INCREMENT)
    degrees -= 2*steps*PS_DISTANCE

    for i in range(0, steps):

        if(actual_speed < speed):
            actual_speed+= PS_INCREMENT

        basic_spin(PS_DISTANCE,spin=spin, speed=actual_speed)
    
    basic_spin(degrees, spin=spin, speed=speed)

    for i in range(0, steps):
        
        basic_spin(PS_DISTANCE, spin=spin, speed=actual_speed, stop=False if i < steps-1 else True)

        if(actual_speed > 0):
            actual_speed-= PS_INCREMENT



# *=> Execution

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