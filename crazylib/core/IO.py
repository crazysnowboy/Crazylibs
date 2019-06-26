import os
import numpy as np
import collections
import chardet
import json
from .files import *
import struct

def ReadJson(file_path):
    with open(file_path, "r", encoding=FileType(file_path)) as f:
        f.seek(0)
        j = json.load(f)
        return j
def WriteJson(file_path,json_data,encode_type="utf-8"):
    with open(file_path, 'w',encoding=encode_type) as json_file:
        json_file.write(json.dumps(json_data,indent=2,ensure_ascii=False))

def ReadSentence(file_path,text_list):
    in_file = open(file_path, 'r',encoding=FileType(file_path))
    lines = in_file.readlines()
    for l in lines:
        l = l.replace("\n","")
        text_list.append(l)
    in_file.close()

def ReadLines(file_path):
    in_file = open(file_path, 'r',encoding=FileType(file_path))
    lines = in_file.readlines()
    return lines

def ReadLines2oneLine(file_path):

    line_out_str=""
    with open(file_path, 'r',encoding=FileType(file_path)) as in_file:
        lines = in_file.readlines()
        for l in lines:
            line_out_str = line_out_str + l

    return line_out_str



def WriteStringLine(save_path,text,cotype="utf-8"):
    print("write string line = ",save_path)
    with open(save_path, 'w+', encoding=cotype) as f:
        f.write(text + '\n')


def Write_String_list_to_file(text_list,save_path,cotype="utf-8"):
    with open(save_path, 'w+', encoding=cotype) as f:
        for text in text_list:
            f.write(text + '\n')



def ReadLines2OneLine(file_path):
    line_out_str=""
    with open(file_path, 'r',encoding=FileType(file_path)) as in_file:
        lines = in_file.readlines()
        for l in lines:
            line_out_str = line_out_str + l

    return line_out_str



def read_vetices_index(file):
    file = open(file, 'r')
    lines = file.readlines()
    data_list=[]
    for i in range(0,len(lines),1):
        id = int(lines[i].replace('\n',''))
        data_list.append(id)
    return data_list


def pickle_save(path,data):
    import pickle
    with open(path, 'wb') as f:
        f.write(pickle.dumps(data))



def pickle_read(path):
    import pickle
    with open(path, 'rb') as f:
        data = pickle.loads(f.read())
        return data



def write_pts(file_path,landmarks):
    with open(file_path,"w") as f:
        line_str="version: 1\n"
        line_str+="n_points:  {:d}\n".format(landmarks.shape[0])
        line_str+="{\n"
        for i in range((landmarks.shape[0])):
            ldmark = landmarks[i,:]
            line_str+="{:5.10f} {:5.10f}\n".format(ldmark[0],ldmark[1])
        line_str += "}\n"
        f.writelines(line_str)


def read_pts(file_path):
    landmarks=[]
    with open(file_path,"r") as f:
        lines = f.readlines()
        if len(lines)>10:
            lines = lines[3:-1]
            for idx,l in enumerate(lines):
                l = l.strip().split(" ")
                pt = np.array([float(v) for v in l])
                landmarks.append(pt)
    return np.array(landmarks)





def write_str_list(file_path,file_path_list):
    with open(file_path,"w") as f:
        for line_str in file_path_list:
            f.writelines(line_str+"\n")




def read_bin_data2(file_path):
    float_data_list = []
    with open(file_path, 'rb') as f:
        float_data = struct.unpack('f', f.read(4))
        float_data_list.append(float_data)
        return float_data_list

def read_bin_data(file_path, byte_n =4):

    data_list = []
    with open(file_path, 'rb') as f:

        byte_data = f.read(byte_n)
        while byte_data != b"":

            float_num = struct.unpack('f', byte_data)
            data_list.append(float_num)

            byte_data = f.read(byte_n)


        return data_list





def pickle_save(path,data):
    import pickle
    with open(path, 'wb') as f:
        f.write(pickle.dumps(data))



def pickle_read(path):
    import pickle
    with open(path, 'rb') as f:
        data = pickle.loads(f.read())
        return data


def read_bin_data(file_path, byte_n =4):

    data_list = []
    with open(file_path, 'rb') as f:

        byte_data = f.read(byte_n)
        while byte_data != b"":

            float_num = struct.unpack('f', byte_data)
            data_list.append(float_num)

            byte_data = f.read(byte_n)


        return data_list