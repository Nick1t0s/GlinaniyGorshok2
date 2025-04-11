def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

import threading
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import configparser
import json
from scipy.fft import rfft, rfftfreq


config = configparser.ConfigParser()
config.read("config.ini")
SERIAL_PORT = config["Serial"]["port"]
BAUD_RATE = config["Serial"]["baud"]

R = int(config["Scheme"]["R"])

data_buffer = deque(maxlen=15000)
# data_buffer.append({"U1":3, "U2":4, "freq1": 100, "freq": 200, "amp1": 2, "amp2": 3})
stop_threads = False

with open("data.txt") as file:
    for line in file:
        ln=line.rstrip("\n")
        x = ln.split(";")
        a = {}
        a["summator"] = arduino_map(int(x[0]), 0, 1023, 0, 5)
        a["filter"] = arduino_map(int(x[1]), 0, 1023, 0, 5)
        a["diode"] = arduino_map(int(x[2]), 0, 1023, 0, 5)
        # data_buffer.append(a)
        if len(data_buffer)!=0:
            mx = max(data_buffer, key=lambda x: a.get("diode")).get("diode")  # Максимально напряжение
            mn = min(data_buffer, key=lambda x: a.get("diode")).get("diode")  # Миниальное напряжение
            sm = sum([x.get("diode") for x in data_buffer])  # Суммарное напряжение
            cnt = len(a)  # Кол-во значений
            mid = sm / cnt  # Ср арифметическое

            a["rippCoef"] = ((mx - mn) / mid) * 100  # коэфицент польсации
            a["I"] = a.get("diode") / R  # Вычисление тока по сопротивлению нагрузки
            a["P"] = a.get("diode") * a.get("I")  # Высисление мощности по току
        data_buffer.append(a)  # Добавляем в буффер данные





def serial_reader():
    global data_buffer, stop_threads

    with open("data.txt") as file:
        for line in file:
            ln = line.rstrip("\n")
            x = ln.split(";")
            a = {}
            a["summator"] = arduino_map(int(x[0]), 0, 1023, 0, 5)
            a["filter"] = arduino_map(int(x[1]), 0, 1023, 0, 5)
            a["diode"] = arduino_map(int(x[2]), 0, 1023, 0, 5)
            # data_buffer.append(a)
            if len(data_buffer) != 0:
                mx = max(data_buffer, key=lambda x: a.get("diode")).get("diode")  # Максимально напряжение
                mn = min(data_buffer, key=lambda x: a.get("diode")).get("diode")  # Миниальное напряжение
                sm = sum([x.get("diode") for x in data_buffer])  # Суммарное напряжение
                cnt = len(a)  # Кол-во значений
                mid = sm / cnt  # Ср арифметическое

                a["rippCoef"] = ((mx - mn) / mid) * 100  # коэфицент польсации
                a["I"] = a.get("diode") / R  # Вычисление тока по сопротивлению нагрузки
                a["P"] = a.get("diode") * a.get("I")  # Высисление мощности по току
            data_buffer.append(a)  # Добавляем в буффер данные



def update_plot(frame):
    # if stop_threads: raise KeyboardInterrupt("Нет порта")
    print("График")

    # print(data_buffer)
    print(len(data_buffer))
    lineSum.set_data(range(len(data_buffer)), [x.get("summator") for x in data_buffer])
    lineFilter.set_data(range(len(data_buffer)), [x.get("filter") for x in data_buffer])
    lineDiod.set_data(range(len(data_buffer)), [x.get("diode") for x in data_buffer])
    try:
        midI = 0
        for i in data_buffer: midI+=i.get("I")
        midI = int(midI/len(data_buffer))
    except:
        midI = "Нет данных"

    try:
        midU = 0
        for i in data_buffer: midU+=i.get("diode")
        midU = int(midU/ len(data_buffer))
    except:
        midU = "Нет данных"

    try:
        midP = 0
        for i in data_buffer: midP+=i.get("diode")
        midP = int(midP/len(data_buffer))
    except:
        midU = "Нет данных"

    try:
        crf = int(data_buffer[-1].get("rippCoef"))
    except:
        crf = "Нет данных"
    coff.set_text(s=f"Коэфицент пульсации: {crf}%")
    I.set_text(s=f"I: {midI}А")
    U.set_text(s=f"U: {midU}В")
    P.set_text(s=f"P: {midP}Вт")
    # fr.set_text(s=f"P: {data_buffer[-1].get("freq1")}Вт")
    # am.set_text(s=f"P: {data_buffer[-1].get("amp1")}Вт")
    # return line

    #----------Фуррие------------
    try:
        SAMPLE_RATE = 1500
        N = 600
        smt = [x.get("summator") for x in data_buffer]
        y = rfft(smt)
        x = rfftfreq(N, 1 / SAMPLE_RATE)

        y = y[1:]
        x = x[1:]
        furri.set_data(range(len(y)), list(map(abs, y)))
    except:
        pass



fig, (ax1, ax2, ax3) = plt.subplots(3)

fig.set_size_inches(12, 5)

lineSum, = ax1.plot([0,1500], [0,5], label = "Сумматор")
lineFilter, = ax1.plot([0,1500], [0,5], label = "Фильтр")
ax1.legend(loc=0)
lineDiod, = ax2.plot([0,1500], [0, 5], label = "Выпрямление")
ax2.legend(loc=0)

furri, = ax3.plot([0,1500], [0, 1000])

coff = plt.figtext(0.005, 0.05, f"Коэфицент пульсации: {1}%")

I = plt.figtext(0.005, 0.15, f"I: {1} A")
U = plt.figtext(0.005, 0.25, f"U: {1} В")
P = plt.figtext(0.005, 0.35, f"P: {1} Вт")
# fr = plt.figtext(0.005, 0.4, f"Freq: {1} Hz")
# am = plt.figtext(0.005, 0.5, f"Amp: {1} В")
serial_thread = threading.Thread(target=serial_reader)
serial_thread.start()


ani = FuncAnimation(fig, update_plot, interval=1)

plt.show()

stop_threads = True
serial_thread.join()
print("Программа завершена")