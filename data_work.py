import matplotlib.pyplot as plt


with open("points_l-yx_cm.txt", "r") as fl:
    data_l = []
    for line in fl:
        l = line.split()
        data_l.append([float(l[0]), float(l[1])])

with open("points_r-yx_cm.txt", "r") as fl:
    data_r = []
    for line in fl:
        l = line.split()
        data_r.append([float(l[0]), float(l[1])])

def create_plot( y, x, title):
    if  type(x) != list or type(y) != list or len(x) != len(y):
        raise Exception("> Not using correctly")

    fig, ax = plt.subplots()
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.scatter(x=0, y= 0, c= "red")
    ax.set_aspect('equal')
    ax.scatter(x=x, y=y)
    ax.set_title(title)


create_plot([l[0] for l in data_r ], [l[1] for l in data_r], "Data R")
create_plot([l[0] for l in data_l], [l[1] for l in data_l], "Data L")
plt.show()