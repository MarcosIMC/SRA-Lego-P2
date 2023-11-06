# progressive movement
PM_INCREMENT=5          # velocity increment every step
PM_DISTANCE=5           # distance every step

# progressive spin
PS_INCREMENT=1          # velocity increment every step
PS_DISTANCE=1           # distance every step


total_distance=0
total_degrees=0

def basic_move(distance, speed):
    global total_distance
    print(speed)
    if speed <= 0:
        print("TOTAL", total_distance)
        raise Exception("AAAAAAAAA")
    total_distance+=distance

def move(distance, speed=50):
    # Para distancias variables necesitamos otro algoritmo que ajuste distancias menores a 2 veces PM_DISTANCE
    actual_speed=0
    steps = int(speed/PM_INCREMENT)
    distance -= 2*steps*PM_DISTANCE

    for i in range(0, steps):

        if(actual_speed < speed):
            actual_speed+= PM_INCREMENT

        basic_move(PM_DISTANCE, speed=actual_speed)
    
    print("distance:", total_distance)
    basic_move(distance, speed=speed)
    print("distance:", total_distance)

    for i in range(0, steps):
        
        basic_move(PM_DISTANCE, speed=actual_speed)

        if(actual_speed > 0):
            actual_speed-= PM_INCREMENT

    print("distance:", total_distance)


def basic_spin(degrees, spin, speed):
    global total_degrees
    print(speed)
    if speed <= 0:
        print("TOTAL", total_distance)
        raise Exception("AAAAAAAAA")
    total_degrees+=degrees


def spin(degrees, spin=100, speed=15):

    actual_speed=0
    steps = int(speed/PS_INCREMENT)
    degrees -= 2*steps*PS_DISTANCE

    for i in range(0, steps):

        if(actual_speed < speed):
            actual_speed+= PS_INCREMENT

        basic_spin(PS_DISTANCE,spin=spin, speed=actual_speed)
    
    print("degrees:", total_degrees)
    basic_spin(degrees, spin=spin, speed=speed)
    print("degrees:", total_degrees)

    for i in range(0, steps):
        
        basic_spin(PS_DISTANCE, spin=spin, speed=actual_speed)

        if(actual_speed > 0):
            actual_speed-= PS_INCREMENT
    
    print("degrees:", total_degrees)


spin(90, 30)

