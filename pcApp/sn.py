from math import *
x=0
a=[]
while x<=pi*2:
    print(x, int(sin(x)*7.5+7.5))
    a.append(int(sin(x)*7.5+7.5))
    x += pi/32
print(a)