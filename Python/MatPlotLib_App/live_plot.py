from itertools import count
import random

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


x = []

y = []

y1 = []

index = count()

plt.style.use("fivethirtyeight")

def animate(i):
    x.append(next(index))
    y.append(random.randint(-5,6))
    y1.append(random.randint(0, 10))
    plt.cla()
    plt.plot(x,y,label = "Channel 1")
    plt.plot(x, y1, label ="Channel 2")
    plt.legend(loc="upper left")
    plt.tight_layout()


fun = FuncAnimation(plt.gcf(),animate,interval=1000)



plt.show()