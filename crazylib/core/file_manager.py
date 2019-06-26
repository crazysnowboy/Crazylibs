import numpy as np
from .files import *
from .basics import *

import random

class FilesManager():

    def __init__(self,file_root,file_name_flag=""):
        self.file_idx = 0
        self.file_info=[]
        files_list = GetFileList(file_root)
        for file in files_list:
            file_dir, sub_dir, full_file_name, bname, ext = ParsePath(file)
            if(file_name_flag in bname or file_name_flag==""):
                name =bname.replace(file_name_flag,"")
                res = (file_dir, sub_dir, full_file_name, bname, ext,name)
                self.file_info.append(res)


    def test(self):

        for idx,exist_file in enumerate(self.file_info):

            file_dir, sub_dir, full_file_name, bname,ext,name= exist_file

    def file_list(self):
        return self.file_info

    def next_file_name(self):
        self.file_idx += 1
        if (self.file_idx>=len(self.file_info)):
            self.file_idx = 0
        path = self.file_info[self.file_idx]

        return os.path.join(path[0],path[2])

    def next_file_name_random(self):
        self.file_idx = int(random.random()*(len(self.file_info)-1))
        if (self.file_idx>=len(self.file_info)):
            self.file_idx = len(self.file_info)-1
        path = self.file_info[self.file_idx]

        return os.path.join(path[0],path[2])


    def pre_file_name(self):
        self.file_idx -= 1
        if (self.file_idx<0):
            self.file_idx = 0

        path =self.file_info[self.file_idx]

        return os.path.join(path[0],path[2])


