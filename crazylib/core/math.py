
from .basics import *
import math
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
    from scipy import interpolate

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

def get_rotation_matrix(eular):
    yaw,pitch,roll =  eular
    yawMatrix = np.matrix([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw), math.cos(yaw), 0],
        [0, 0, 1]
    ])

    pitchMatrix = np.matrix([
        [math.cos(pitch), 0, math.sin(pitch)],
        [0, 1, 0],
        [-math.sin(pitch), 0, math.cos(pitch)]
    ])

    rollMatrix = np.matrix([
        [1, 0, 0],
        [0, math.cos(roll), -math.sin(roll)],
        [0, math.sin(roll), math.cos(roll)]
    ])

    R = yawMatrix * pitchMatrix * rollMatrix
    return R




def euler_to_quaternion(eular):

    yaw,pitch,roll =  eular

    qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
    qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
    qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
    qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)

    return np.array([qw,qx, qy, qz])

def quaternion_to_euler(quaternion):
    w, x, y, z = quaternion
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.asin(t2)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)

    # res = np.array([yaw, roll, pitch])
    # res = np.array([yaw, pitch, roll])
    # res = np.array([pitch,yaw, roll])
    # res = np.array([pitch,roll, yaw])
    res = np.array([roll,pitch, yaw])
    # res = np.array([roll,yaw, pitch])

    return res