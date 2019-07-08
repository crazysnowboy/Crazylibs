import os
import numpy as np
import collections
import chardet
import json
from scipy import interpolate


def get_this_path(file=__file__):
    abs_path = os.path.abspath(file)
    file_dir, sub_dir, full_file_name, bname, ext = ParsePath(abs_path,False)
    return file_dir

def makedirs(path):
    if os.path.exists(path) is False:
        os.makedirs(path)
def remove_dir(path):
    os.removedirs(path)

def list_curren_dir(root,prefix=None):

    dirs=[]
    if os.path.exists(root)==False:
        return []
    contents =os.listdir(root)
    for content in contents:
        sub_path = os.path.join(root, content)
        if os.path.isdir(sub_path)==True:
            if prefix is not None:
                if prefix in content:
                    return content
            else:
                dirs.append(content)
    if prefix is None:
        return dirs
    else:
        return []


def list_all_dirs(root, dirs_list,empty_dirs_list):
    # print(path)

    sub_path_list =os.listdir(root)
    cnt=0
    for dir in sub_path_list:
        sub_path = os.path.join(root, dir)
        if os.path.isdir(sub_path):
            if os.listdir(sub_path):
                list_all_dirs(sub_path,dirs_list, empty_dirs_list)
            else:
                empty_dirs_list.append(sub_path)
        else:
            cnt = cnt +1

    if cnt==len(sub_path_list):
        dirs_list.append(root)


def GetFolderList(root_path, sub_dirs=[""]):
    folder_list = []
    empty_folder_list = []

    for sub_dir in sub_dirs:
        path = os.path.join(root_path, sub_dir)
        list_all_dirs(path, folder_list,empty_folder_list)
    return folder_list,empty_folder_list


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


def get_file_dir(file_path):
    file_name = os.path.basename(file_path)
    return file_path.replace(file_name,"")[:-1]





