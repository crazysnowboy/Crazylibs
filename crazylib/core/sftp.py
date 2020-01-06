import numpy as np


def ReadSSHConfig(if_print):
    import os
    from .IO import ReadLines2OneLine
    home_dir = os.environ['HOME']
    ssh_config_file = os.path.join(home_dir, ".ssh/config")
    config_lines = ReadLines2OneLine(ssh_config_file, 1)

    host_dict = {}
    host_list = config_lines.split("Host ")
    for host_str in host_list:
        if len(host_str) > 0:

            host_lines = host_str.split("\n")

            if if_print:
                print("---------------")
                print(host_lines)
            host_dict[host_lines[0]] = {
                "ip": host_lines[1].split(" ")[-1],
                "port": host_lines[2].split(" ")[-1],
                "user": host_lines[3].split(" ")[-1],
                "id_rsa": host_lines[4].split(" ")[-1].replace("~",home_dir)
            }
    if if_print:
        for host in host_dict.keys():
            print(host, host_dict[host])
    return host_dict

class SFTP_Manager():
    def __init__(self,ip,user,passwd,port):
        import paramiko
        self._tansporter = paramiko.Transport((ip, port))
        self._tansporter.connect(username=user, password=passwd)
        self._sftp = paramiko.SFTPClient.from_transport(self._tansporter)

    def __del__(self):
        self._tansporter.close()

    def list_dir(self,root_path,show=True):
        dirs = self._sftp.listdir(root_path)
        if show is True:
            for dir in dirs:
                print(dir)

        return dirs

    def down_file(self,server_path, local_path):
        try:
            self._sftp.get(server_path, local_path)
        except ZeroDivisionError as err:
            print('Exception: ', err)
