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

# leds
from ev3dev2.led import Leds

from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor import INPUT_1


# oth
from time import sleep
import time

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
usSensor = UltrasonicSensor(INPUT_2)
btn = Button()
colorSensor = ColorSensor(INPUT_4)
steer.gyro = GyroSensor(INPUT_1)

# steer.gyro.calibrate()

distances = []
sound.beep()
while not btn.any(): pass

sleep(1)

position_history = []
start_time = time.time()

while not btn.any():
    distance = usSensor.distance_centimeters_continuous
    angle = steer.gyro.angle
    print("{:.2f} ; {:.2f} ;".format(distance, angle))
    position_history.append(
        (time.time() - start_time, distance, angle))
    #distances.append(usSensor.distance_centimeters_continuous)

with open('position_history.csv', 'w') as fp:
    fp.write('\n'.join('{},{}'.format(x[0], x[1]) for x in position_history))
