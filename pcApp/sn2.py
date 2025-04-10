rez = [1, 7.5, 15, 12, 24, 72]

for Ros in rez:
    for R1 in rez:
        for R2 in rez:
            for R3 in rez:
                res = (2.5*Ros/R1+5*Ros/R2+2.5*Ros/R3)
                if res==5:
                    print(Ros, R1, R2, R3, res)

# 12 24 24 5.0