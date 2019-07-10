
from .core.file_manager import *
from .core.basics import *
from .core.dirs import *
from .core.IO import *
from .core.deploy import *
from .core.math import *
from .core.vi import *
from .core.log import *



def CreateSubModule(create_file_name,dirs_list=["core"]):
    file_dir = get_this_path(__file__)
    create_file_path = get_this_path(__file__)
    import_str = "from "
    for sub_dir in dirs_list:
        create_file_path = os.path.join(create_file_path,sub_dir)
        import_str = import_str+"."+sub_dir

    import_str = import_str +"." + create_file_name.replace(".py","")+" import *\n"

    create_file_path = file_dir
    for sub_dir in dirs_list:
        create_file_path = os.path.join(create_file_path,sub_dir)

    print("create_file_path =",create_file_path)
    if not os.path.exists(create_file_path):
        os.makedirs(create_file_path)

    abs_file_name = os.path.join(create_file_path,create_file_name)
    print("abs_file_name =",abs_file_name)
    with open(abs_file_name,"a") as f:
        f.write("import numpy as np")
        pass


    this_file_path = os.path.abspath(__file__)
    this_file = ReadLines2OneLine(this_file_path)
    this_file = import_str + this_file
    WriteStringLine(this_file_path,this_file)


def git_add_commit_push(cmd_list=[]):
    # this code is very crazy
    this_path = get_file_dir(get_this_path())
    os.chdir(os.path.join(this_path, "../"))

    os.system("git log")
    os.system("git status >log.txt")
    log_str_line_list = ReadLines("log.txt")

    add_file_info = ""
    for log_str in log_str_line_list:
        if "modified:" in log_str:
            add_file_info += (log_str.replace("modified:", "").strip() + " ")

    if len(cmd_list) == 0:
        cmd_list = [
            "git config --global credential.helper store",
            "git status",
            "git branch temp",
            "git checkout temp",
            "git add " + add_file_info,
            "git status",
            "git commit -m 'modified " + add_file_info + "'",
            "git pull origin master:test",
            "git checkout master",
            "git merge test",
            "git merge temp",
            "git checkout master",
            "git push origin HEAD:master"
        ]

    for cmd in cmd_list:
        print("crazy_cmd = ",cmd)
        os.system(cmd)

def git_pull(cmd_list=[]):
    # this code is very crazy
    this_path = get_file_dir(get_this_path())
    os.chdir(os.path.join(this_path, "../"))

    if len(cmd_list) == 0:
        cmd_list = [
            "git checkout master",
            "git pull origin master"
        ]

    for cmd in cmd_list:
        os.system(cmd)


def deploy():
    import crazylib
    crazylib.deploy_link_to_annconda(src_lib_path="/home/collin/Documents/my_projects/dl_3dface/core/utils",
                                     dst_lib_name="mytools")

    
def Test():

    CreateSubModule(["core"],"Expression.py")
















