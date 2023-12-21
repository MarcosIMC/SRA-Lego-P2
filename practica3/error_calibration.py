import math
import numpy as np

L=1
L_TIMES=4


rx = []
# points_r-yx_cm.txt
# points_r-yx_sistematico.txt
with open("points_r-yx_sistematico.txt", "r") as fl:
    for line in fl:
        sp = line.split()
        rx.append([float(sp[1])])

lx = []
# points_l-yx_cm.txt
# points_l-yx_sistematico.txt
with open("points_l-yx_sistematico.txt", "r") as fl:
    for line in fl:
        sp = line.split()
        lx.append([float(sp[1])])

rx= np.array(rx)
lx = np.array(lx)

rx_mean = np.mean(rx)/100
lx_mean = np.mean(lx)/100

beta = ((rx_mean - lx_mean)/(-L*L_TIMES))

# Error en la proporcion del tamaño de las ruedas
R = (L*.5)/math.sin(beta/2)
Ed = (R+beta/2)/(R-beta/2)

# Error en el tamaño de la base
alpha = ((rx_mean + lx_mean)/(-L_TIMES*L))*(180/math.pi)
Eb = 90/(90-alpha)

print("Ed:", Ed)
print("Eb:", Eb)