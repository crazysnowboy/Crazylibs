
import os
import numpy as np
from .pyCrazyCPP import *
from . import pyCrazyCPP


def Ndarray2ImageMatrix(arraya_data):


    ImageMatrix = pyCrazyCPP.ImageMatrix()
    arraya_data = arraya_data.astype("float64")
    if(len(arraya_data.shape)==3):
        all_chanels =arraya_data.shape[-1]
        for i in range(0,all_chanels,1):
            Image_Python2CPP(arraya_data[:,:,i],i,ImageMatrix)
    return ImageMatrix


def ImageMatrix2Ndarray(iamge_matrix,channels=3):

    data_size = ImageMatrixCPP2Python(2,iamge_matrix,0,"GetLength")
    rows = int(data_size[0])
    cols = int(data_size[1])
    image_array = np.zeros((rows,cols,channels),np.uint8)

    for c in range(channels):
        data = ImageMatrixCPP2Python(rows * cols,iamge_matrix,c,"GetData")
        if cols >1:
            data = data.reshape(rows,cols)
        image_array[:,:,c] = data.astype("uint8")


    return image_array


def Ndarray2DMat(arraya_data_src):
    import copy

    arraya_data = copy.deepcopy(arraya_data_src)
    dmat = DMatrix()
    arraya_data = arraya_data.astype("float64")

    if len(arraya_data.shape)==1:
        arraya_data =  arraya_data.reshape(arraya_data.shape[0],1)

    NumpyData_Python2CPP(arraya_data,dmat)
    return dmat

def DMat2Ndarray(DMat):

    data_size = NUmpyDataCPP2Python(2,DMat,"GetLength")
    rows = int(data_size[0])
    cols = int(data_size[1])
    data = NUmpyDataCPP2Python(rows * cols,DMat,"GetData")
    if cols >1:
        data = data.reshape(rows,cols)
    return data



def DMat2List(DMat):


    data_size = NUmpyDataCPP2Python(2,DMat,"GetLength")
    rows = int(data_size[0])
    cols = int(data_size[1])
    data = NUmpyDataCPP2Python(rows * cols,DMat,"GetData")
    print("data shape = ",data.shape)
    if cols >1:
        data = data.reshape(rows,cols)

    data_list=[]
    for r in range(data.shape[0]):
        d = data[r,:]
        if data.shape[1]==2:
            d_tuple = (d[0],d[1])
        elif data.shape[1]==3:
            d_tuple = (d[0],d[1],d[2])

        data_list.append(d_tuple)
    return data_list


def ReadMatbin(root_path):

    dmat = LoadMatBinary2Dmat(root_path)
    ndarray = DMat2Ndarray(dmat)
    return ndarray

