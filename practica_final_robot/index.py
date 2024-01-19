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
from evdev3dev2.sensor import INPUT_1

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
usSensor = UltrasonicSensor(INPUT_2)
btn = Button()
colorSensor = ColorSensor(INPUT_4)
gyro = GyroSensor(INPUT_1)


# *=> vars

# defs

# functions
def move(distance, speed=15, brake=True, block=False):

    distance*=10

    degrees= 360*distance/P_RIGHT_WHEEL

    steer.on_for_degrees(0, speed=speed, degrees=degrees, brake=brake, block=block)

def spin(degrees, spin=100, speed=15, brake=True, block=False):

    degrees_left= P_WHEELS*degrees/P_LEFT_WHEEL
    degrees_right= P_WHEELS*degrees/P_RIGHT_WHEEL
    
    steer.on_for_degrees(spin, speed=speed, degrees=degrees_right, brake=brake, block=block)




# 1. giro de busqueda
# 2. preparar el brazo
# 3. Movimiento hacia la lata
# 4. Golpe a la lata
# 5. Salir del circulo
    
distances = []
    
def search_spin(min_gap):

    distances.append("SEARCH_SPIN")

    motor = Motor(OUTPUT_A)

    distances.append("FIRST")

    # Girar primero hacia un lado
    spin(45, -100, 10, True, True)

    sound.beep()
    sleep(1)

    # Si resulta que el objeto se encuentra justo en el borde
    measure = usSensor.distance_centimeters_continuous
    distances.append(measure)
    while(measure <= min_gap):
        spin(5, -100, 10, True, True)
        measure = usSensor.distance_centimeters_continuous
        distances.append(measure)

    sound.beep()
    sleep(1)
    # Encontramos el borde izquierdo del objeto

    # Buscamos hacia la derecha algo
    spin(5, 100, 15, True, True)
    measure = usSensor.distance_centimeters_continuous
    distances.append(measure)
    while(measure >= min_gap):
        measure = usSensor.distance_centimeters_continuous
        distances.append(measure)
        spin(5, 100, 15, True, True)

    sound.beep()
    sleep(1)
    idx = 0
    spin(8, 100, 10, True, True)
    measure = usSensor.distance_centimeters_continuous
    distances.append(measure)

    while(measure <= min_gap):
        spin(5, 100, 10, True, True)
        measure = usSensor.distance_centimeters_continuous
        distances.append(measure)
        idx+=1
    # Encontramos el otro borde del objeto
    sound.beep()
    sleep(1)
        
    spin(idx*2.5, -100, 15, True, True)
    sound.beep()
    sleep(1)

    return True


def lift_arm():
    arm.on_for_degrees(speed=20, degrees=100*Z_REL, brake=True, block=True)

intensities = []
def move_to_goal():
    intensities.append("MOVE_TO_GOAL")
    motor = Motor(OUTPUT_A)
    speed = 50
    leds.set_color( "LEFT", "YELLOW", pct=1)

    intensities.append("FIRST")
    move(10, speed, block=False)
    steer.run_forever()
    
    intens = colorSensor.reflected_light_intensity
    intensities.append(intens)
    while intens  < COLOR_GAP:
        intens = colorSensor.reflected_light_intensity
        intensities.append(intens)

    leds.set_color( "LEFT", "RED", pct=1)

    intensities.append("SECOND")
    move(10, speed, block=False)
    steer.run_forever()
    
    intens = colorSensor.reflected_light_intensity
    intensities.append(intens)
    while intens > COLOR_GAP_OUT:
        intens = colorSensor.reflected_light_intensity
        intensities.append(intens)
    leds.set_color( "LEFT", "GREEN", pct=1)

    intensities.append("THIRD")
    while True:
        
        intens = colorSensor.reflected_light_intensity
        intensities.append(intens)
        if intens > COLOR_GAP: break

        move(10, speed, block=False)
        steer.run_timed(time_sp=3000)

        while(intens < COLOR_GAP):
            if(not motor.is_running):
                search_spin(30)
                break
            intens = colorSensor.reflected_light_intensity
            intensities.append(intens)

        steer.stop()

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

leds.all_off()
leds.set_color( "LEFT","GREEN", pct=1)
sound.beep()

while not btn.any(): pass

lift_arm()

while not btn.any(): pass

sound.beep()



if ( not search_spin(80)):
    move(-5, 20, True, False)
    exit()
sound.beep()
move_to_goal()

"""
move(-15, 30, True, True)
search_spin(30)
measure = usSensor.distance_centimeters_continuous
move(measure, 10, True, True)
spin(5, -100, 5, True, True)
 """
while(not hit_goal()):
    lift_arm()
    sleep(1)
    move(-15, 30, True, True)
    search_spin(30)
    measure = usSensor.distance_centimeters_continuous
    move(measure, 10, True, True)

leds.set_color( "RIGHT", "YELLOW", pct=1)
sound.beep()
if(move_out()): leds.set_color( "LEFT", "GREEN", pct=1)

sound.beep()
# encendemos el led cuando esté fuera del círculo exterior 

while not btn.any(): pass



print(distances, file=open("distances.txt", "a"))
print(intensities, file=open("intensity.txt", "a"))