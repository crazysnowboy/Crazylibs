import numpy as np
import json

class CrazyDict():
    def __init__(self,json_file=None,config_dict=None):
        self._config_dict_init=dict()
        if config_dict is not None:
            self._config_dict =config_dict
        else:
            self._config_dict=dict()

        if json_file is not None:
            self.from_json_file(json_file)

    def traverse_dict_to_get(self, dict_data, key_search):
        if type(dict_data) is CrazyDict:
            key_list = dict_data.config_dict.keys()
        elif type(dict_data) is dict:
            key_list = dict_data.keys()
        elif type(dict_data) is list:
            return dict_data
        else:
            raise ValueError("dic_data is ",type(dict_data)," which is not supported now")
        for key in key_list:
            ele = dict_data[key]
            # print(key,"---------",key_search)
            if key == key_search:
                # print("=====================")
                if type(ele) is dict:
                    return CrazyDict(config_dict=ele)
                else:
                    return ele
            else:
                if type(ele) is dict:
                    res = self.traverse_dict_to_get(ele, key_search)
                    if res is not None:
                        return res

    def traverse_dict_to_set(self, dict_data, key_search,value):
        for key in dict_data.keys():
            ele = dict_data[key]
            if key == key_search:
                if type(ele) is dict and type(value) is CrazyDict:
                    dict_data[key] = value.get_dict()
                else:
                    dict_data[key]=value
                return True
            else:
                if type(ele) is dict:
                    res = self.traverse_dict_to_set(ele, key_search,value)
                    if res is True:
                        return True


    def __call__(self, key_input):
        key_list = key_input.split(":")
        dst = self._config_dict
        for key in key_list:
            dst = self.traverse_dict_to_get(dst, key)


        if dst is None:
            raise ValueError("Can not find key = "+key)
        return dst

    def keys(self):
        return self._config_dict.keys()

    def __getitem__(self, item):
        return self.__call__(item)

    def __setitem__(self, key_input, value):
        key_list = key_input.split(":")
        dst = self._config_dict
        if len(key_list)>1:
            for key in key_list:
                dst = self.traverse_dict_to_set(dst, key,value)
        else:
            res = self.traverse_dict_to_set(dst, key_input, value)
            if res is not True:
                self._config_dict[key_input]=value


    def to_json_file(self, path):
        with open(path, 'w') as f:
            json.dump(self._config_dict, f, indent=4,sort_keys=True)

    def from_json_file(self, path):
        with open(path, 'r') as f:
            self._config_dict = json.load(fp=f)

    def __str__(self):
        return str(json.dumps(self._config_dict, indent=4,sort_keys=True))

    def get_dict(self):
        return self._config_dict




