# SRA-Lego-P2
Práctica 2 - Lego

## Iteración 1
Como primera aproximación, creamos el código utilizando el **MoveTank** pero teníamos el problema de que al tener dos llamadas seguidas al método **.on(ref_motor_izq, ref_motor_der)** el movimiento no era uniforme, lo cuál no tenía la sensación de fluidez que queríamos.

## Iteración 2
Para la segunda iteración, vimos en la documentación, que existe la opción de **on_for_dregrees(left_speed, right_speed, degrees, brake=True, block=True)**, del objeto **MoveTank**, aquí mejoramos el giro del robot, haciendo que fuera más fluido, pero manteníamos los errores en el arranque del mismo, cada vez que se quedaba parado, tanto en el punto inicial, como cuando se finalizaba el giro.

## Iteración 3
Para la tercera iteración, probamos el método **LargeMotor(address=None, name_pattern='*', name_exact=False, kwargs)** de forma individual para cada motor. El comportamiento del robot, al tener un inicio independiente, hacía que uno de ellos avanzara primero mientras el otro seguía parado, por lo que se producía un pequeño giro. Además cuando terminaba cada ejecución, se producía un pequeño giro inverso al del inicio, ya que la rueda que giró primero, se paraba también antes que la otra.

## Iteración 4 
En la cuarta iteración, decidimos cambiar el movimiento del robot a utilizando el objeto **MoveSteering**, con este objeto combinado con el método **on_for_degrees(steering, speed, degrees, brake=True, block=True)**, conseguimos hacer que ambos motores puedan arrancar al mismo tiempo, por lo que evitamos el problema de las iteraciones anteriores, donde se producía un pequeños movimiento de arrastre, producido por el arranque inicial de unos de los motores por tener sus llamadas independientes. Además, conseguimos que el giro sea de forma menos brusca en esta iteración.

# Enlaces de referencia
- https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html#move-steering
