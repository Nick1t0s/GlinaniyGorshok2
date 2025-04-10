import threading
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")
SERIAL_PORT = config["Serial"]["port"]
BAUD_RATE = config["Serial"]["baud"]

R = config["Scheme"]["R"]

data_buffer = deque(maxlen=15000)
data_buffer.append({"U1":3, "U2":4, "freq1": 100, "freq": 200, "amp1": 2, "amp2": 3})
stop_threads = False


def serial_reader():
    global data_buffer, stop_threads

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"{SERIAL_PORT}/{BAUD_RATE}")

        while not stop_threads:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    try:
                        dt = line.split(",")
                        data = {}

                        # Парсим данные
                        data["diode"] = dt[2]
                        data["filter"] = dt[1]
                        data["summator"] = dt[0]

                        # Для анализа готового сигнала
                        mx = max(data, key = lambda x: x.get("diode")).get("diode") # Максимально напряжение
                        mn = min(data, key = lambda x: x.get("diode")).get("diode") # Миниальное напряжение
                        sm = sum([x.get("U2") for x in data_buffer]) # Суммарное напряжение
                        cnt = len(data) # Кол-во значений

                        mid = sm/cnt # Ср арифметическое

                        data["rippCoef"] = ((mx-mn)/mid)*100 # коэфицент польсации
                        data["I"] = data.get("diode")/R # Вычисление тока по сопротивлению нагрузки
                        data["P"] = data.get("diode")*data.get("I") # Высисление мощности по току
                        data_buffer.append(data) # Добавляем в буффер данные


                    except Exception as e:
                        print(f"Wrong: {line}, \n Eer: e")
            except UnicodeDecodeError as e:
                print(e)

        ser.close()
        print("Close")
    except serial.SerialException as e:
        print(f"Ошибка serial порта: {e}")
        stop_threads = True

def update_plot(frame):
    # if stop_threads: raise KeyboardInterrupt("Нет порта")
    print("График")

    print(data_buffer)

    lineSum.set_data(range(len(data_buffer)), [x.get("summator") for x in data_buffer])
    lineFilter.set_data(range(len(data_buffer)), [x.get("filter") for x in data_buffer])
    lineDiod.set_data(range(len(data_buffer)), [x.get("diode") for x in data_buffer])
    try:
        midI = 0
        for i in data_buffer: midI+=i.get("I")
        midI /= len(data_buffer)
    except:
        midI = "Нет данных"

    try:
        midU = 0
        for i in data_buffer: midU+=i.get("U")
        midU /= len(data_buffer)
    except:
        midU = "Нет данных"

    try:
        midP = 0
        for i in data_buffer: midP+=i.get("U")
        midP /= len(data_buffer)
    except:
        midU = "Нет данных"

    coff.set_text(s=f"Коэфицент пульсации: {data_buffer[-1].get("rippCoef")}%")
    I.set_text(s=f"I: {midI}А")
    U.set_text(s=f"U: {midU}В")
    P.set_text(s=f"P: {midP}Вт")
    # fr.set_text(s=f"P: {data_buffer[-1].get("freq1")}Вт")
    # am.set_text(s=f"P: {data_buffer[-1].get("amp1")}Вт")
    # return line


fig, (ax1, ax2) = plt.subplots(2)

fig.set_size_inches(12, 5)

lineSum, = ax1.plot([0,1], [0,5], label = "Сумматор")
lineFilter, = ax1.plot([0,1], [0,4], label = "Фильтр")
ax1.legend(loc=0)
lineDiod, = ax2.plot([0,1], [1, 2], label = "Выпрямление")
ax2.legend(loc=0)

coff = plt.figtext(0.005, 0.0, f"Коэфицент пульсации: {1}%")

I = plt.figtext(0.005, 0.1, f"I: {1} A")
U = plt.figtext(0.005, 0.2, f"U: {1} В")
P = plt.figtext(0.005, 0.3, f"P: {1} Вт")
# fr = plt.figtext(0.005, 0.4, f"Freq: {1} Hz")
# am = plt.figtext(0.005, 0.5, f"Amp: {1} В")
serial_thread = threading.Thread(target=serial_reader)
serial_thread.start()


# ani = FuncAnimation(fig, update_plot, interval=1)

plt.show()

stop_threads = True
serial_thread.join()
print("Программа завершена")