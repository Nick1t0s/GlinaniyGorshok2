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
                        data = json.loads(line)
                        # U1 - int
                        # U2 - int
                        # freq1 - int
                        # freq2 - int
                        # amp1 - int
                        # amp2 - int

                        mx = max(data, key = lambda x: x.get("U2")).get("U2")
                        mn = min(data, key = lambda x: x.get("U2")).get("U2")
                        sm = sum([x.get("U2") for x in data_buffer])
                        cnt = len(data)

                        mid = sm/cnt

                        data["rippCoef"] = ((mx-mn)/mid)*100
                        data["I"] = data.get("U2")/R
                        data["P"] = data.get("U2")*data.get("I")
                        data_buffer.append(data)


                    except Exception as e:
                        print(f"Wrong: {line}, \n Eer: e")
            except UnicodeDecodeError:
                print(UnicodeDecodeError)

        ser.close()
        print("Close")
    except serial.SerialException as e:
        print(f"Ошибка serial порта: {e}")
        stop_threads = True

def update_plot(frame):
    # if stop_threads: raise KeyboardInterrupt("Нет порта")
    print("График")

    print(data_buffer)

    lineU1.set_data(range(len(data_buffer)), [x.get("U1") for x in data_buffer])
    lineU2.set_data(range(len(data_buffer)), [x.get("U2") for x in data_buffer])


    coff.update(s=f"Коэфицент пульсации: {data_buffer[-1].get("rippCoef")}%")
    I.update(s=f"I: {data_buffer[-1].get("I")}А")
    U.update(s=f"U: {data_buffer[-1].get("U2")}В")
    P.update(s=f"P: {data_buffer[-1].get("P")}Вт")
    fr.update(s=f"P: {data_buffer[-1].get("freq1")}Вт")
    am.update(s=f"P: {data_buffer[-1].get("amp1")}Вт")
    # return line


fig, (ax1, ax2) = plt.subplots(2)

fig.set_size_inches(12, 5)

lineU1, = ax1.plot([0,1], [0,5])



lineU2, = ax2.plot([0,1], [1, 2])

coff = plt.figtext(0.005, 0.0, f"Коэфицент пульсации: {1}%")

I = plt.figtext(0.005, 0.1, f"I: {1} A")
U = plt.figtext(0.005, 0.2, f"U: {1} В")
P = plt.figtext(0.005, 0.3, f"P: {1} Вт")
fr = plt.figtext(0.005, 0.4, f"Freq: {1} Hz")
am = plt.figtext(0.005, 0.5, f"Amp: {1} В")

serial_thread = threading.Thread(target=serial_reader)
serial_thread.start()


ani = FuncAnimation(fig, update_plot, interval=1)

plt.show()

stop_threads = True
serial_thread.join()
print("Программа завершена")