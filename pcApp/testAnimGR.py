import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, (ax, ax2) = plt.subplots(2) #create two axes
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro')
ln2, = ax2.plot([], [], 'go') # added

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    ax2.set_xlim(0, 2*np.pi) # added
    ax2.set_ylim(-1, 1) # added
    return ln,ln2 # added ln2

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    ln2.set_data(xdata, ydata) # added
    return ln, ln2 #added ln2

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()