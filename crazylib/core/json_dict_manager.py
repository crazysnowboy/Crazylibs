import os
import json
import datetime
from collections import OrderedDict

class JsonDictManager():
    def __init__(self,data_dict_init=None):
        self.__force_init_keys=[]
        if data_dict_init is not None:
            self.set_from_dict(data_dict_init)
        else:
            self.__data_dict = OrderedDict()

        self._is_force_assign = False
        self.crazy_key_list=[]
        self.log_color={
                        "HEADER":'\033[95m',
                        "OKBLUE":'\033[94m',
                        "OKGREEN":'\033[92m',
                        "WARNING":'\033[93m',
                        "FAIL":'\033[91m',
                        "ENDC":'\033[0m',
                        "BOLD":'\033[1m',
                        "UNDERLINE":'\033[4m'
                        }


    def set_force_keys(self,keys):
        self.__force_init_keys = keys
    def set_from_dict(self,input_dict):
        if type(input_dict) is not OrderedDict:
            self.__data_dict = self._traverse_convert_dict_to_ordered_dict(input_dict)
        else:
            self.__data_dict = input_dict

    def _log_i(self,*infos):
        info_str=""
        for info in infos:
            info_str+=str(info)
        print(self.log_color["HEADER"]+info_str+self.log_color["ENDC"])

    def _log_w(self,*infos):
        info_str=""
        for info in infos:
            info_str+=str(info)
        print(self.log_color["WARNING"]+info_str+self.log_color["ENDC"])

    def _log_e(self,*infos):
        info_str=""
        for info in infos:
            info_str+=str(info)
        print(self.log_color["FAIL"]+info_str+self.log_color["ENDC"])

    def get_crazy_keys_list(self):
        self.crazy_key_list=[]
        dict_data = self.__data_dict
        for key in dict_data.keys():
            assert type(key)==str
            self.crazy_key_list.append(key)
            if type(dict_data[key]) is OrderedDict:
                self._traverse_dict_to_get_crazy_keys(dict_data[key], key)

        return self.crazy_key_list
    def _set_exist_key_value(self,dict_data,key,value):
        if type(value) == type(dict_data[key]):
            dict_data[key] = value
            return True
        else:
            if self._is_force_assign == True:
                self._is_force_assign = False
                return True
            raise ValueError("setting exist key =",key," error! type of setting value is: ", type(value), " but value in dict is :",
                             type(dict_data[key]))
    def _traverse_dict_to_get_crazy_keys(self,dict_data, parent_key):
        for key in dict_data.keys():
            assert type(key)==str
            new_key = parent_key+":"+key
            self.crazy_key_list.append(new_key)
            if type(dict_data[key]) is OrderedDict:
                self._traverse_dict_to_get_crazy_keys(dict_data[key], new_key)
    def _traverse_dict_to_set_from_crazy_keys(self,dict_data, parent_key,crazy_key,value):
        for key in dict_data.keys():
            assert type(key)==str
            new_key = parent_key+":"+key
            if new_key==crazy_key:
                return self._set_exist_key_value(dict_data,key,value)
            if type(dict_data[key]) is OrderedDict:
                self._traverse_dict_to_set_from_crazy_keys(dict_data[key], new_key,crazy_key,value)

        return False
    def _get_value_from_crazy_key(self,crazy_key):
        this_dict = self.__data_dict
        key_list = crazy_key.split(":")
        for idx, key in enumerate(key_list):
            if idx < len(key_list) - 1:
                if key not in this_dict.keys():
                    raise ValueError("can not find crazy key:",crazy_key," in key:",key)
                this_dict = this_dict[key]
            else:
                if key not in this_dict.keys():
                    raise ValueError("can not find crazy key:",crazy_key," in key:",key)
                return this_dict[key]
    def _set_value_from_crazy_key(self,crazy_key,value):
        dict_data = self.__data_dict
        ret = False
        for idx,key in enumerate(dict_data.keys()):
            assert type(key)==str
            if key==crazy_key:
                return self._set_exist_key_value(dict_data,key,value)
            elif type(dict_data[key]) is OrderedDict:
                ret = self._traverse_dict_to_set_from_crazy_keys(dict_data[key], key,crazy_key,value)
                if ret == True:
                    return True

        if ret == False:
            this_dict = dict_data
            key_list = crazy_key.split(":")
            for idx,key in enumerate(key_list):
                if idx < len(key_list) - 1:
                    if key not in this_dict.keys():
                        this_dict[key] = OrderedDict()
                    this_dict =  this_dict[key]
                else:
                    this_dict[key] = value
    def _traverse_dict_to_get_value(self, dict_data, key_search):

        dict_keys = dict_data.keys()
        for idx,key in enumerate(dict_keys):
            if key == key_search:
                if type(dict_data[key]) is OrderedDict:
                    return JsonDictManager(data_dict_init=dict_data[key])
                else:
                    return dict_data[key]

            elif type(dict_data[key]) is OrderedDict:
                res = self._traverse_dict_to_get_value(dict_data[key], key_search)
                if res is not None:
                    return res

        return None
    def _find_crazy_key_in_key_list(self,key_search,with_raise=False):

        crazy_key_list = self.get_crazy_keys_list()
        crazy_key_candidate_list = []
        for crazy_key in crazy_key_list:
            if key_search in crazy_key:
                crazy_key_candidate_list.append(crazy_key)


        matched_key_crazy_key_list = []
        for crazy_key in crazy_key_candidate_list:
            key_list = crazy_key.split(":")
            for key in key_list:
                if key == key_search:
                    matched_key_crazy_key_list.append(crazy_key)

        if len(matched_key_crazy_key_list) == 0:
            if with_raise==True:
                raise ValueError("can not find value with key: ",key_search)
            else:
                return None
        if len(matched_key_crazy_key_list) == 1:
            return matched_key_crazy_key_list[0]
        elif len(matched_key_crazy_key_list) > 1:
            min_len = 10000
            min_matched = None
            for matched in matched_key_crazy_key_list:
                if min_len > len(matched):
                    min_len = len(matched)
                    min_matched = matched

            for matched in matched_key_crazy_key_list:
                if min_matched != matched:
                    if min_matched not in matched:
                        raise ValueError("exist duplicated key: ", matched_key_crazy_key_list)


            return min_matched
    def _traverse_key_list_to_get_value(self, key_search):
        crazy_key = self._find_crazy_key_in_key_list(key_search,with_raise=True)
        res = self._get_value_from_crazy_key(crazy_key)
        if type(res) is OrderedDict:
            return JsonDictManager(data_dict_init=res)
        else:
            return res
    def _traverse_key_list_to_set_value(self, key_setting,value):
        crazy_key = self._find_crazy_key_in_key_list(key_setting,with_raise=False)
        if crazy_key is not None:
            self._set_value_from_crazy_key(crazy_key,value)
        else:
            self.__data_dict[key_setting] = value

    def _traverse_convert_dict_to_ordered_dict(self, dict_data):
        if hasattr(dict_data, "keys"):
            if type(dict_data) is dict:
                dict_data = OrderedDict(dict_data)
            for key in dict_data.keys():
                if hasattr(dict_data[key],"keys"):
                    dict_data[key] = self._traverse_convert_dict_to_ordered_dict(dict_data[key])
        return dict_data

    def _get_value_from_key(self,key):
        return self._traverse_key_list_to_get_value(key)

    def _set_value_from_key(self,key,value):
        self._traverse_key_list_to_set_value(key,value)

    def get_dict(self):
        return self.__data_dict
    def clear(self):
        self.__data_dict={}

    def crazy_keys(self):
        return self.get_crazy_keys_list()

    def keys(self):
        return self.__data_dict.keys()

    def __str__(self):
        return str(json.dumps(self.__data_dict, indent=4,sort_keys=True))



    def __call__(self, key_input):
        key_list = key_input.split(":")
        if len(key_list)>1:
            return self._get_value_from_crazy_key(key_input)
        else:
            return self._get_value_from_key(key_input)


    def __getitem__(self, item):
        value = self.__call__(item)
        if type(value) is JsonDictManager:
            if "ndarray" in value.keys() and len(value.keys()) == 1:
                import numpy as np
                value = np.array(value["ndarray"])
        return value

    def force_assign(self,key_input,value):
        self._is_force_assign = True
        self.__setitem__(key_input,value)

    def __setitem__(self, key_input, value):
        import numpy as np
        if type(value) is np.ndarray:
            value = {
                "ndarray":value.tolist(),
            }
        value = self._traverse_convert_dict_to_ordered_dict(value)
        key_list = key_input.split(":")
        if len(key_list)>1:
            self._set_value_from_crazy_key(key_input,value)
        else:
            self._set_value_from_key(key_input,value)


    def to_json_file(self, path):
        self._log_i("save to: ",path)
        with open(path, 'w') as f:
            json.dump(self.__data_dict, f, indent=4,sort_keys=True)

    def from_json_file(self, path,mode="overwrite"):
        with open(path, 'r') as f:
            if mode=="overwrite":
                tmp_dict = json.load(fp=f,object_pairs_hook=OrderedDict)

                self.__data_dict =  self.force_key_settting(tmp_dict)

            elif mode=="add":
                tmp_dict = json.load(fp=f,object_pairs_hook=OrderedDict)
                item_name = os.path.basename(path).split(".")[0]
                self.__data_dict[item_name] = tmp_dict

    def force_key_settting(self,tmp_dict):
        tmp_pack = JsonDictManager(tmp_dict)
        ForceSetting=False
        for force_key in self.__force_init_keys:
            ForceSetting = True
            self._log_i("force setting key:",force_key)
            value = JsonDictManager(self.__data_dict)[force_key]
            if type(value) is JsonDictManager:
                value = value.get_dict()
            tmp_pack[force_key]=value
        if ForceSetting:
            # self._log_i("force setted:",self)
            pass

        return tmp_pack.get_dict()
