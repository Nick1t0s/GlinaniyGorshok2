import math
C = [3.3*10**-9, 2.4*10**-8, 0.00001]
R = [1000, 12000, 24000, 72000]
for C2 in C:
    for C1 in C:
        for R1 in R:
            for R2 in R:
                for R3 in R:
                    K = (R3/R1)*(C1/(C1+C2))
                    dw = (1/R3) * (1/C1+1/C2)
                    fd = 1/(2*math.pi*math.sqrt(R1*R2*C1*C2))
                    if 1400<=fd<=1500:
                        print(fd, C1, C2, R1, R2, R3) #Расчет полосового фильтра для 1500 Hz