import os
import numpy as np
import collections
import chardet
import json
import matplotlib.pyplot as plt
from scipy import interpolate
from .basics import *

def my_smooth_3rd(x):
    f0 = x[0]
    f1 = x[-1]
    f0p = x[1]-x[0]
    f1p = x[-1]-x[-2]

    d = f0
    c = f0p

    A = f1 - f0 -f0p
    B = f1p - f0p

    a = B-2*A
    b = 3*A - B

    t = np.linspace(0,1,len(x))

    y = a*t**3 + b*t**2 + c*t +d

    return y


def GenerateWeight(n,fre):
    ratial = 0.0
    t_step = 0
    base_n = 10000
    y = np.zeros((base_n), dtype=np.float32)

    for i in range(0, base_n):
        y_data = 1.0
        if (i >= ratial * base_n):
            ti = float(t_step) / base_n
            t_step = t_step + 1
            y_data = abs(np.sin(ti * np.pi / 2 * fre))
            if (Equal(y_data, 1.0)):
                ratial = 1.0 - ti
        y[i] = y_data

    x = np.linspace(0, 1, base_n)
    xnew = np.linspace(0, 1, n)
    #"nearest","zero","slinear","quadratic","cubic"
    f = interpolate.interp1d(x, y, kind="quadratic")

    ynew = f(xnew)
    return ynew
