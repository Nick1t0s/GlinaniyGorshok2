from math import *

C = [3.3*10**-9, 2.4*10**-8, 0.00001]
R = [1000, 12000, 24000, 72000]

for R1 in R:
    for C1 in C:
        x = 1/(2*pi*R1*C1)
        if x<1400:
            print(1/(2*pi*R1*C1))