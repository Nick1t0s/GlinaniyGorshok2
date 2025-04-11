import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
import numpy as np




f = open("data.txt")
lines = f.readlines()
l = len(lines)
s = 0
summat = [0] * 600
filt = [0] * 600
vypr = [0] * 600

while (True):
    for i in range(600):
        if s == l:
            s = 0
        summat[i], filt[i], vypr[i] = map(int, lines[s].split(';'))
        s += 1
    plt.plot(summat)
    plt.show()


    SAMPLE_RATE = 1500
    N = 600
    y = rfft(summat)
    x = rfftfreq(N, 1 / SAMPLE_RATE)

    y = y[1:]
    x = x[1:]

    plt.plot(x, np.abs(y))
    plt.show()

    break



f.close
