import os
import numpy as np
import collections
import chardet
import json
import matplotlib.pyplot as plt
from scipy import interpolate
import time
import datetime


def get_file_modified_time(filename):

    ModifiedTime = time.localtime(os.stat(filename).st_mtime)
    y = time.strftime('%Y', ModifiedTime)
    m = time.strftime('%m', ModifiedTime)
    d = time.strftime('%d', ModifiedTime)
    H = time.strftime('%H', ModifiedTime)
    M = time.strftime('%M', ModifiedTime)
    S = time.strftime('%S', ModifiedTime)
    # all_seconds = int(H) * 3600 + int(m) * 60 + int(S)

    time_res = datetime.datetime(int(y), int(m), int(d), int(H), int(M), int(S))

    all_seconds = int(time.strftime('%s', ModifiedTime))
    return all_seconds,time_res



def DrawLine(y,flag,ymin,ymax):
    x = np.linspace(0, y.shape[0], y.shape[0])
    plt.plot(x, y)
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.ylim((ymin,ymax))
    plt.title(flag)
    plt.show()


def Dict2Ndarray(dict,flag):
    array = np.empty(0)
    for key in dict.keys():
        if flag in key:
            array = np.append(array, dict[key])
    return  array


def PrintDict(dict,flag=""):
    str_out = "%10s---->"%flag
    for key in dict.keys():
        if "Brow" in key:
            dat =dict[key]
            str_out = str_out + " %8d " % int(dat)
    print(str_out)

def Equal(v1,v2):
    epslo =0.0001
    if(v1<v2+epslo and v1 > v2-epslo):
        return True
    else:
        return False



def get_instance(module, name, config, *args):
    return getattr(module, config[name]['type'])(*args, **config[name]['args'])


def ParsePath(file_path,ifPrint=False):
    from pathlib import Path
    from pathlib import PurePath

    full_file_name = os.path.basename(file_path)
    bname = Path(full_file_name).stem
    sub_dir = PurePath(file_path).parts[-2]
    file_dir = file_path.replace(full_file_name, "")[:-1]
    extention = full_file_name.replace(bname+".","")

    if(ifPrint==True):
        print("file_dir= ", file_dir)
        print("sub_dir= ", sub_dir)
        print("full_file_name= ", full_file_name)
        print("bname= ", bname)
        print("extention= ", extention)

    return file_dir, sub_dir, full_file_name, bname,extention

def get_seg_data(data,pointer,num,return_list=False):
    offset_pointer = num

    res_data = data[pointer[0]:pointer[0]+offset_pointer]

    pointer[0] += offset_pointer

    if return_list == True:
        return res_data
    else:
        return np.array(res_data)
