import numpy as np


class SFTP_Manager():
    def __init__(self,ip,user,passwd):
        import paramiko
        self._tansporter = paramiko.Transport((ip, 22))
        self._tansporter.connect(username=user, password=passwd)
        self._sftp = paramiko.SFTPClient.from_transport(self._tansporter)

    def __del__(self):
        self._tansporter.close()

    def list_dir(self,root_path):
        dirs = self._sftp.listdir(root_path)
        for dir in dirs:
            print(dir)

        return dirs

    def down_file(self,server_path, local_path):
        try:
            self._sftp.get(server_path, local_path)
        except ZeroDivisionError as err:
            print('Exception: ', err)
