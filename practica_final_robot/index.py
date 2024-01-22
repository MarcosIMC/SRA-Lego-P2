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
usSensor = UltrasonicSensor(INPUT_2)
btn = Button()
colorSensor = ColorSensor(INPUT_4)
gyro = GyroSensor(INPUT_1)
motorL, motorR = Motor(OUTPUT_A), Motor(OUTPUT_D)

def reset_motor():
    motorL.reset()
    motorR.reset()

    motorL.ramp_up_sp =     1000
    motorL.ramp_down_sp =   1000
    motorR.ramp_up_sp =     1000
    motorR.ramp_down_sp =   1000

reset_motor()



# *=> vars

# defs

# functions
def move(distance, speed=15, brake=True, block=False):

    if(distance < 0 or speed < 0):
        motorL.speed_sp = -motorL.max_speed
        motorR.speed_sp = motorR.max_speed

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

    
def search_spin(min_gap, *, offset1=55, speed1=13, speed2=10, offset2= 10, second_lap=False, fast_exit = False):

    SLEEP_PERIOD = .002
    ANGLE_OFFSET = 2

    best_measure = float("inf")
    best_measure_angle = 0

    spin(offset1, -100, 80, True, False)
    while motorL.is_running: pass

    leds.set_color("LEFT", "GREEN", pct=1)
    spin(offset1*2, 100, speed1, True, False)
    while motorL.is_running:
        sleep(SLEEP_PERIOD)
        measure = usSensor.distance_centimeters_continuous
 
        if( measure < best_measure and measure < min_gap ):
            best_measure = measure
            best_measure_angle = gyro.angle
            leds.set_color("LEFT", "RED", pct=1)
            if (fast_exit ): break
           

    if(best_measure > min_gap):
        spin(offset1, -100, 80, True, False)
        return False
    
    dO = abs(best_measure_angle-gyro.angle)
    Oo = offset2 if second_lap else 0
    turning_sense = -100 if (dO + Oo) <= 180 else 100
    O = (dO + Oo) if turning_sense == -100 else (dO - Oo)
  
    spin( O, turning_sense, 80, True, True)

    if not second_lap:
        dist = usSensor.distance_centimeters_continuous
        return dist if dist <= min_gap else None

    # segunda vuelta

    best_measure = float("inf")
    best_measure_angle = 0

    while motorL.is_running: pass

    leds.set_color("LEFT", "GREEN")
    spin(offset2*2, 100, speed2, True, False)
    while motorL.is_running:
        sleep(SLEEP_PERIOD)
        measure = usSensor.distance_centimeters_continuous

        if( measure < best_measure and measure < min_gap ):
            best_measure = measure
            best_measure_angle = gyro.angle
            leds.set_color("LEFT", "RED", pct=1)


    dO = abs(best_measure_angle-gyro.angle)
    turning_sense = -100 if dO <= 180 else 100
    O = dO  if turning_sense == -100 else (360 - dO)

    spin( O ,turning_sense, 60, True, True)

    dist = usSensor.distance_centimeters_continuous
    
    return dist if dist <= min_gap else None


def lift_arm():
    arm.on_for_degrees(speed=20, degrees=100*Z_REL, brake=True, block=True)

intensities = []
def move_to_goal():
    intensities.append("MOVE_TO_GOAL")
    speed = 70
    TIMEOUT=2500
    leds.set_color( "LEFT", "YELLOW", pct=1)

    intensities.append("FIRST")
    move(10, speed, block=False)
    steer.run_forever()
    
    intens = colorSensor.reflected_light_intensity
    intensities.append(intens)
    while intens < COLOR_GAP:
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
        steer.run_timed(time_sp=TIMEOUT)

        while(intens < COLOR_GAP):
            if(not motorL.is_running):
                return False
            intens = colorSensor.reflected_light_intensity
            intensities.append(intens)

        steer.stop()

    steer.stop()
    return True


def hit_goal():

    MOVE_OFFSET = 3

    # if(usSensor.distance_centimeters_continuous > 5):
    #     move(5, -15, True, True)
    #     dist = search_spin(30, offset1=45, speed1=10, fast_exit=True)
    #     while(not search_spin(30, offset1=45, speed1=10, fast_exit=True)):
    #          move(5, -15, True, True)
    #          dist = search_spin(30, offset1=45, speed1=10, fast_exit=True)
    #     move( dist - MOVE_OFFSET, 10, brake=True, block=True)
   
    arm.on_for_degrees(speed=35, degrees=-97*Z_REL, brake=True, block=False)
    while(arm.is_running):
        if( ts.is_pressed ): return True
    
    return False

def move_out():

    motorL, motorR = Motor( OUTPUT_A), Motor(OUTPUT_D)
    motorL.speed_sp = -motorL.max_speed
    motorR.speed_sp = -motorR.max_speed

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
    
MOVE_OFFSET = 3

while True:

    leds.all_off()
    while not btn.any(): pass
    sleep(2)

    leds.set_color( "LEFT","GREEN", pct=1)
    lift_arm()
    sound.beep()

    while ( not search_spin(100, second_lap=True)): pass

    sound.beep()
    if(not move_to_goal()):
        dist = search_spin(30, offset1=180, speed1=10, second_lap=True, fast_exit=True)
        # FIXME Quitar esto cuando
        if(not dist): leds.set_color( "LEFT" ,"YELLOW")
        sleep(1)
        #====== 
        while(not dist): dist = search_spin(30, offset1=180, speed1=10, second_lap=True)
        move(dist-MOVE_OFFSET, 10, True, True) 
    else:
        dist = search_spin(30, offset1=40, speed1=10, second_lap=True)
        while(not dist):
            move(5, -30, True, True)
            dist = search_spin(30, offset1=40, speed1=10, second_lap=True)

    move(dist-MOVE_OFFSET, 10, True, True)   

    times = 0
    while(not hit_goal()):
        lift_arm()
        sleep(10)
        reset_motor()
        move(-10, 30, True, True)

        if(times > 5):
            dist = search_spin(15, offset1=180, speed1=15, second_lap=True, fast_exit=True)
            times = 0
        else:
            dist = search_spin(30, offset1=45, speed1=10, second_lap=True)

            while(not dist and times < 5):
                dist = search_spin(30, offset1=45, speed1=10, second_lap=True, fast_exit=True)
                times += 1

        move(dist-MOVE_OFFSET, 15, True, True)
        times+=1


    leds.set_color( "RIGHT", "YELLOW", pct=1)
    sound.beep()

    if(move_out()): leds.set_color( "LEFT", "GREEN", pct=1)

    leds.set_color( "RIGHT", "GREEN", pct=1)
    sound.beep()
