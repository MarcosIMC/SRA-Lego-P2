import math
import numpy as np

L=1
L_TIMES=4


rx = []
with open("points_r-yx_sistematico.txt", "r") as fl:
    for line in fl:
        sp = line.split()
        rx.append([float(sp[1])])

lx = []
with open("points_l-yx_sistematico.txt", "r") as fl:
    for line in fl:
        sp = line.split()
        lx.append([float(sp[1])])

rx= np.array(rx)
lx = np.array(lx)

rx_mean = np.mean(rx)
lx_mean = np.mean(lx)

beta = ((rx_mean - lx_mean)/-L*L_TIMES)*(180/math.pi)

# Error en la proporcion del tamaño de las ruedas
R = (L/2)/math.sin(beta/2)
Ed = (R+beta/2)/(R-beta/2)

# Error en el tamaño de la base
alpha = ((rx_mean + lx_mean)/-L_TIMES*L)*(180/math.pi)
Eb = 90/(90-alpha)

print("Ed:", Ed)
print("Eb:", Eb)