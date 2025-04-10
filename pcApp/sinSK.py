def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def rnd(x):
    if x%1>=0.5:
        return ceil(x)
    else:
        return floor(x)
from math import *
x = 0
new = []
while x<=2*pi:
    am = arduino_map(sin(x), -1, 1, 0, 7)
    print(am, rnd(am))
    new.append(rnd(am))
    x+=2*pi/16
print(new)