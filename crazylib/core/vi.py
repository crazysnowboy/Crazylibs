import matplotlib.pyplot as plt
import numpy as np
def DrawLine(y,flag,ymin,ymax):
    x = np.linspace(0, y.shape[0], y.shape[0])
    plt.plot(x, y)
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.ylim((ymin,ymax))
    plt.title(flag)
    plt.show()