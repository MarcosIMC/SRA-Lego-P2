#!/usr/bin/env python3

# *=> imports
from enum import Enum
import math

import datetime

from ev3dev2.button import Button
from ev3dev2.sound import Sound

# movement (left: A, right: D)
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, Motor
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

# gyroscope
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor import INPUT_1

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

COLOR_GAP=17
COLOR_GAP_OUT=10

Z_REL=(-40/24)


leds = Leds()
sound = Sound()
ts = TouchSensor(INPUT_3)
arm = MediumMotor(OUTPUT_C)
steer = MoveSteering( OUTPUT_A, OUTPUT_D)
motorL, motorR = Motor(OUTPUT_A), Motor(OUTPUT_D)
usSensor = UltrasonicSensor(INPUT_2)
btn = Button()
colorSensor = ColorSensor(INPUT_4)
gyro = GyroSensor(INPUT_1)
#gyro.calibrate()



def move(distance, speed=15, brake=True, block=False):

    distance*=10

    degrees= 360*distance/P_RIGHT_WHEEL

    steer.on_for_degrees(0, speed=speed, degrees=degrees, brake=brake, block=block)


def spin(degrees, spin=100, speed=15, brake=True, block=False):

    degrees_left= P_WHEELS*degrees/P_LEFT_WHEEL
    degrees_right= P_WHEELS*degrees/P_RIGHT_WHEEL
    
    steer.on_for_degrees(spin, speed=speed, degrees=degrees_right, brake=brake, block=block)



def search_spin(min_gap):


    best_measure = float("inf")
    best_measure_angle = 0

    spin(55, -100, 15, True, False)
    while motorL.is_running: pass

    init_angle = gyro.angle
    # print("initial angle: {}".format(gyro.angle))
    # sleep(2)
    count=0

    spin(110, 100, 15, True, False)
    while motorL.is_running:
        sleep(.005)
        measure = usSensor.distance_centimeters_continuous
        # print("angle: {}".format(gyro.angle))
        count+=1
        if( measure < best_measure ):
            best_measure = measure
            best_measure_angle = gyro.angle
            print("")
            print("best angle: {}".format(best_measure_angle))
            print("init angle: {}".format(init_angle))
            print("distance: {}".format(best_measure))
        
    

    # print("final angle: {}".format(gyro.angle))
    # print("best_measured_ancle: {}".format(best_measure_angle))
    # print("best_measure:{}".format(best_measure))
    # sleep(2)

    if(best_measure > min_gap):
        spin(55, -100, 15, True, False)
        return False
    
    spin(abs(best_measure_angle-gyro.angle), -100, 15, True, True)

    print("final FINAL: {}".format(gyro.angle))

    print("count {}".format(count))
    
    return best_measure


sound.beep()
while not btn.any(): pass

sleep(1)

while True:
    if(search_spin(110)): sound.beep()
    else:
        sound.beep()
        sound.beep()
    while not btn.any(): pass



# while not btn.any():
#     print("{}".format(gyro.angle))
# exit()