import os
import numpy as np
import collections
import chardet
import json
import matplotlib.pyplot as plt
from scipy import interpolate
import time
import datetime
import copy
import cv2
class Cropper():
    def __init__(self):
        pass
    def crop_with_landmarks(self,image,landmarks,extend_scale=1.2):


        bbox = self.caculate_bbox(image,landmarks)

        # self.draw_bbox(image,bbox)
        new_cropped, new_bbox_for_crop = self.crop_with_extend_bbox(image,bbox,extend_scale)
        cropped_landmarks = copy.deepcopy(landmarks)

        (x_min, x_max, y_min, y_max) = new_bbox_for_crop
        cropped_landmarks[:,0]-=x_min
        cropped_landmarks[:,1]-=y_min

        return new_cropped,cropped_landmarks

    def crop_with_extend_bbox(self,image_input,bbox_input,extend_scale):

        image = copy.deepcopy(image_input)
        (x_min, x_max, y_min, y_max) =copy.deepcopy( bbox_input)
        x_size = np.abs(x_max - x_min)
        y_size = np.abs(y_max - y_min)
        x_center = x_min + x_size//2
        y_center = y_min + y_size//2

        new_x_size = int(x_size *extend_scale)
        new_y_size = int(y_size *extend_scale)



        new_x_min = x_center - new_x_size//2
        new_x_max = x_center + new_x_size//2

        new_y_min = y_center - new_y_size//2
        new_y_max = y_center + new_y_size//2

        bbox_input_new= (new_x_min, new_x_max,
                         new_y_min, new_y_max)

        croped_image,new_bbox_for_crop = self.crop_with_bbox(image,bbox_input_new)

        new_cropped = np.zeros((new_y_size, new_x_size,3), dtype=np.uint8)

        (x_min, x_max, y_min, y_max) = new_bbox_for_crop

        new_cropped_x_min = new_x_size // 2 + (x_min - x_center)
        new_cropped_x_max = new_x_size // 2 + (x_max - x_center)

        new_cropped_y_min = new_y_size // 2 + (y_min - y_center)
        new_cropped_y_max = new_y_size // 2 + (y_max - y_center)

        new_cropped[new_cropped_y_min:new_cropped_y_max,
                    new_cropped_x_min:new_cropped_x_max,:] = croped_image


        return new_cropped,new_bbox_for_crop




    def draw_bbox(self,image_input,bbox_input):
        (x_min, x_max, y_min, y_max) = copy.deepcopy(bbox_input)
        image_draw = copy.deepcopy(image_input)

        print((x_min, x_max, y_min, y_max))
        cv2.rectangle(image_draw,(x_min,y_min),(x_max,y_max),(0,255,0),1)
        cv2.namedWindow("image_bbox",0)
        cv2.imshow("image_bbox",image_draw)
        key = cv2.waitKey(0)



    def caculate_bbox(self,image,landmarks):

        x = landmarks[:,0].astype("int32")
        x_used = x[x>0]
        x_used = x_used[x_used< image.shape[1]]


        x_min ,x_max= np.min(x_used),np.max(x_used)


        y = landmarks[:,1].astype("int32")
        y_used = y[y>0]
        y_used = y_used[y_used< image.shape[0]]


        y_min ,y_max= np.min(y_used),np.max(y_used)



        return (x_min,x_max,y_min,y_max)

    def check_bbox(self,image,bbox_input):

        (x_min, x_max, y_min, y_max) =copy.deepcopy( bbox_input)

        if x_max > image.shape[1]:
            x_max = int(image.shape[1] - 1)

        if y_max > image.shape[0]:
            y_max = int(image.shape[0] - 1)

        if x_min < 0:
            x_min = int(0)

        if y_min < 0:
            y_min = int(0)

        bbox=(int(x_min), int(x_max), int(y_min), int(y_max))
        return bbox

    def crop_with_bbox(self,image_input,bbox_input):

        image = copy.deepcopy(image_input)
        new_bbox_for_crop =self.check_bbox(image,bbox_input)
        (x_min, x_max, y_min, y_max) = new_bbox_for_crop
        croped = image[y_min:y_max,x_min:x_max,:]

        return croped,new_bbox_for_crop




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
