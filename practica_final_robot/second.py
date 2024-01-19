#!/usr/bin/env python3

# *=> imports
import math

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

# oth
from time import sleep

# *=> conts

D_LEFT_WHEEL=55
D_RIGHT_WHEEL=56

D_WHEELS=125

Z_REL=(-40/24)

P_LEFT_WHEEL=D_LEFT_WHEEL*math.pi
P_RIGHT_WHEEL=D_RIGHT_WHEEL*math.pi

P_WHEELS=D_WHEELS*math.pi

COLOR_GAP=17
COLOR_GAP_OUT=10

leds = Leds()
sound = Sound()
ts = TouchSensor(INPUT_3)
arm = MediumMotor(OUTPUT_C)
steer = MoveSteering( OUTPUT_A, OUTPUT_D)
usSensor = UltrasonicSensor(INPUT_2)
btn = Button()
colorSensor = ColorSensor(INPUT_4)

# For move_in() function 
threshold_moveIn = 20

# *=> basic functions
def move(distance, speed=15, brake=True, block=False):

    distance*=10

    degrees= 360*distance/P_RIGHT_WHEEL

    steer.on_for_degrees(0, speed=speed, degrees=degrees, brake=brake, block=block)

def spin(degrees, spin=100, speed=15, brake=True, block=False):

    degrees_left= P_WHEELS*degrees/P_LEFT_WHEEL
    degrees_right= P_WHEELS*degrees/P_RIGHT_WHEEL
    
    steer.on_for_degrees(spin, speed=speed, degrees=degrees_right, brake=brake, block=block)

# new algorithm functions
def search_spin(min_gap):
    spin(90,100,15,True,False)
    val = check(min_gap)
    if val > 0: return val
    spin(180,-100,15,True,False)
    return check()

def lift_arm():
    arm.on_for_degrees(speed=20, degrees=100*Z_REL, brake=True, block=True)

def check(min_gap):
    while(steer.duty_cycle > 0):
        measure = usSensor.distance_centimeters_continuous
        if measure < min_gap:
            steer.stop()
            return measure
    return 0

def move_in(dist):
    
    while dist >= threshold_moveIn:
        move(dist-threshold_moveIn,20,True,True)
        dist = search_spin(dist)
    move(10,10,True,False)
    steer.run_forever()
    aux = 0
    while colorSensor.reflected_light_intensity < COLOR_GAP:
        #Timeout hecho rápido
        aux = aux +1
        if aux > 10000:
            steer.stop()
            exit()
        pass
    steer.stop()
    
def hit_goal():
    arm.on_for_degrees(speed=35, degrees=-97*Z_REL, brake=True, block=False)
    while(arm.is_running):
        if( ts.is_pressed ): return True
    
    return False

def move_out():

    motorL, motorR = Motor( OUTPUT_A), Motor(OUTPUT_D)
    motorL.speed_sp = -motorL.max_speed*.8
    motorR.speed_sp = -motorR.max_speed*.8

    leds.set_color("RIGHT", "RED")
    # detecta la entrada a la linea interior
    
    steer.run_forever()
    while colorSensor.reflected_light_intensity < COLOR_GAP: pass
    
    # detecta salida de linea interior
    while colorSensor.reflected_light_intensity > COLOR_GAP_OUT: pass

    # detecta ultima linea
    while colorSensor.reflected_light_intensity < COLOR_GAP: pass
    steer.stop()


#*=> main
    
while not btn.any(): pass

leds.all_off()
leds.set_color( "LEFT", "YELLOW", pct=1)

lift_arm()

leds.set_color( "RIGHT", "YELLOW", pct=1)

dist = search_spin(120)
if dist == 0:
    # TODO: Hay que hacer que siga buscando en vez de tirar para atrás
    move(-5, 20, True, False)
    exit()
# Finds the target and starts to move to it
sound.beep()
leds.set_color( "LEFT", "GREEN", pct=1)
move_in(dist)

# Is in front of the target
sound.beep()
leds.set_color( "RIGHT", "GREEN", pct=1)

while not hit_goal():
    sleep(3)
    move_in(threshold_moveIn)
# Has hit the target
sound.beep()
leds.set_color( "LEFT", "YELLOW", pct=1)

if move_out(): leds.set_color( "LEFT", "GREEN", pct=1)

while not btn.any(): pass
