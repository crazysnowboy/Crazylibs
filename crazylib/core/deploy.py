import os
from .dirs import list_curren_dir,get_file_dir

def deploy_link_to_annconda(src_lib_path,dst_lib_name):

    if src_lib_path=="":
        raise ValueError("src_lib_path needed")
   
    if dst_lib_name=="":
        raise ValueError("dst_lib_name needed")
    
    envs_dict = os.environ
    home_path= envs_dict["HOME"]

    conda_dirs=[".conda","anaconda3"]
    for conda_dir in conda_dirs:
        conda_root=os.path.join(home_path,conda_dir)
        envs = os.path.join(conda_root,"envs")
        envs_dirs = list_curren_dir(envs)
        this_path = get_file_dir(__file__)

        for env_dir in envs_dirs:
            lib_dir=os.path.join(envs,env_dir,"lib")

            python_dir = list_curren_dir(lib_dir,"python")
            site_package_dir = os.path.join(lib_dir,python_dir,"site-packages")

            dst_lib_path = os.path.join(site_package_dir,dst_lib_name)

            cmd_rm ="rm -rf " +dst_lib_path
            print(cmd_rm)
            os.system(cmd_rm)
            
            cmd_link = "ln -s " + src_lib_path +" " +dst_lib_path
            print(cmd_link)
            os.system(cmd_link)