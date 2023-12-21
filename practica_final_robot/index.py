#!/usr/bin/env python3

# *=> imports

from ev3dev2.button import Button

# movement (left: A, right: D)
from ev3dev2.motor import OUTPUT_A, OUTPUT_D

# arm movement (-degrees: front, degrees: back)
from ev3dev2.motor import MediumMotor, OUTPUT_C

# color sensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1
class ColorSensor(Enum):
    NO_COLOR = 0
    BLACK = 1
    WHITE = 6

# touch sensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor import INPUT_3

# us sensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2

# leds
from ev3dev2.led import Leds
class Color(Enum):
    L_RED="RED"
    L_GREEN="GREEN"
    L_YELLOW="YELLOW"


# display
from ev3dev2.console import Console
import ev3dev2.fonts  as fonts

# oth
from time import sleep


# *=> conts

ts = TouchSensor(INPUT_3)
leds = Leds()
arm = MediumMotor(OUTPUT_C)
console = Console()


# *=> vars



#*=> main

console.set_font('Lat15-Terminus32x16.psf.gz', True)
console.text_at("Holaasdfasdfadasdfsdafasdfasdfsaf", column=1, row=1, reset_console=True)


while True:
    if ts.is_pressed:
#        display.draw.text((10, 10), "Touched" )
        break
    else:
        pass
        # display.draw.text((10, 10), "Not Touched" )


sleep(2)


arm.on_for_degrees(5, 40, brake=True, block= True)
sleep(1)
arm.on_for_degrees(5, -35, brake=True, block= True)

