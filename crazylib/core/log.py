global __log_level

def set_log_level(level):
    global __log_level
    __log_level = level


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def __get_clickable_path(CallerFilePath,CallerlineNumber):
    return 'File "' + CallerFilePath + '", line ' + CallerlineNumber + ','

def __get_time_info():
    import time
    localtime = time.asctime( time.localtime(time.time()) )
    return  "["+str(localtime)+"] "


def log_out(data,log_level_input):
    global __log_level
    if log_level_input <=  __log_level:
        print(data)




def log_error(*infos):
    import sys
    CallerFilePath = sys._getframe().f_back.f_code.co_filename
    CallerfuncName = sys._getframe().f_back.f_code.co_name
    CallerlineNumber = str(sys._getframe().f_back.f_lineno)
    info_str = __get_clickable_path(CallerFilePath,CallerlineNumber) + 'in ' + CallerfuncName + ''
    log_out(bcolors.OKBLUE+info_str+bcolors.ENDC, 0)
    info_str = __get_time_info()+" I "
    for info in infos:
        info_str+=str(info)
    log_out(bcolors.FAIL+info_str+bcolors.ENDC)
def log_waring(*infos):
    import sys
    CallerFilePath = sys._getframe().f_back.f_code.co_filename
    CallerfuncName = sys._getframe().f_back.f_code.co_name
    CallerlineNumber = str(sys._getframe().f_back.f_lineno)
    info_str = __get_clickable_path(CallerFilePath,CallerlineNumber) + 'in ' + CallerfuncName + ''
    log_out(bcolors.OKBLUE+info_str+bcolors.ENDC, 0)
    info_str = __get_time_info()+" I "
    for info in infos:
        info_str+=str(info)
    log_out(bcolors.WARNING+info_str+bcolors.ENDC)

def log_info(*infos,level):
    import sys
    CallerFilePath = sys._getframe().f_back.f_code.co_filename
    CallerfuncName = sys._getframe().f_back.f_code.co_name
    CallerlineNumber = str(sys._getframe().f_back.f_lineno)
    info_str = __get_clickable_path(CallerFilePath,CallerlineNumber) + 'in ' + CallerfuncName + ''
    log_out(bcolors.OKBLUE+info_str+bcolors.ENDC, level)
    info_str = __get_time_info()+" I "

    for info in infos:
        info_str+=str(info)

    info_str += "\n"
    log_out(bcolors.OKGREEN+info_str+bcolors.ENDC, level)




def print_list(data_list,max_n=-1):
    for idx,data in enumerate(data_list):
        if idx>max_n and max_n>0:
            break
        print(data)
