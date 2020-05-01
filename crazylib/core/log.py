global __log_level
__log_level = 0

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
    
    
def get_color(color_info):
    """
        数值表示的参数含义：
        显示方式: 0（默认值）、1（高亮）、22（非粗体）、4（下划线）、24（非下划线）、 5（闪烁）、25（非闪烁）、7（反显）、27（非反显）
        前景色: 30（黑色）、31（红色）、32（绿色）、 33（黄色）、34（蓝色）、35（洋 红）、36（青色）、37（白色）
        背景色: 40（黑色）、41（红色）、42（绿色）、 43（黄色）、44（蓝色）、45（洋 红）、46（青色）、47（白色）

        常见开头格式：
        \033[0m            默认字体正常显示，不高亮
        \033[32;0m       红色字体正常显示
        \033[1;32;40m  显示方式: 高亮    字体前景色：绿色  背景色：黑色
        \033[0;31;46m  显示方式: 正常    字体前景色：红色  背景色：青色
    """
    if color_info=="green":
        return bcolors.OKGREEN
    elif color_info=="blue":
        return bcolors.OKBLUE
    elif color_info=="red":
        return '\033[91m'
    else:
        return '\033['+color_info+"m"

    

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


def get_caller(calling_level):
    import sys
    CallerFilePath = sys._getframe(calling_level).f_back.f_code.co_filename
    CallerfuncName = sys._getframe(calling_level).f_back.f_code.co_name
    CallerlineNumber = str(sys._getframe(calling_level).f_back.f_lineno)
    return  CallerFilePath,CallerlineNumber,CallerfuncName

def get_caller_str(calling_level):
    CallerFilePath, CallerlineNumber, CallerfuncName = get_caller(calling_level)
    return __get_clickable_path(CallerFilePath,CallerlineNumber) + 'in ' + CallerfuncName + ''


def log_error(*infos,log_level_input=0):
    info_str = get_caller_str(2)
    log_out(bcolors.FAIL+info_str+bcolors.ENDC, log_level_input)
    info_str = __get_time_info()+" E "
    for info in infos:
        info_str+=str(info)
    info_str += "\n"
    log_out(bcolors.FAIL+info_str+bcolors.ENDC,log_level_input=log_level_input)
def log_waring(*infos):
    info_str = get_caller_str(2)

    log_out(bcolors.WARNING+info_str+bcolors.ENDC, 0)
    info_str = __get_time_info()+" W "
    for info in infos:
        info_str+=str(info)
    info_str += "\n"
    log_out(bcolors.WARNING+info_str+bcolors.ENDC,log_level_input=0)

def log_info(*infos,level=0, with_file_info = True,color=None,relative_caller_level = 0):
    """
    color: the color info of text from std::cout
        example:
            color="green"
            color="blue"
            color="red"
            color="0;31;46"
            
        details:
            数值表示的参数含义：
            显示方式: 0（默认值）、1（高亮）、22（非粗体）、4（下划线）、24（非下划线）、 5（闪烁）、25（非闪烁）、7（反显）、27（非反显）
            前景色: 30（黑色）、31（红色）、32（绿色）、 33（黄色）、34（蓝色）、35（洋 红）、36（青色）、37（白色）
            背景色: 40（黑色）、41（红色）、42（绿色）、 43（黄色）、44（蓝色）、45（洋 红）、46（青色）、47（白色）

            常见开头格式：
            0m            默认字体正常显示，不高亮
            32;0       红色字体正常显示
            1;32;40  显示方式: 高亮    字体前景色：绿色  背景色：黑色
            0;31;46  显示方式: 正常    字体前景色：红色  背景色：青色
    """
    if with_file_info ==True:
        info_str = get_caller_str(2 - relative_caller_level)
        log_out(bcolors.OKBLUE+info_str+bcolors.ENDC, level)

    info_str = __get_time_info()+" I "

    for info in infos:
        info_str+=str(info)

    info_str += "\n"
    if color is None:
        color = bcolors.OKGREEN
    else:
        color = get_color(color)
    log_out(color+info_str+bcolors.ENDC, level)




def print_list(data_list,max_n=-1,info=""):
    log_info(info, with_file_info=True,relative_caller_level=-1)
    for idx,data in enumerate(data_list):
        if idx>max_n and max_n>0:
            break
        log_info("[",idx,"]: ",data,with_file_info=False)


def assert_eq(v1,v2):
    if v1 != v2:
        raise ValueError(v1," is not equal to ",v2)