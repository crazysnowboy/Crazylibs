import os



def GetFileList(root_path, sub_dirs=[""],suffix=None):
    file_path_list = []
    for sub_dir in sub_dirs:
        path = os.path.join(root_path, sub_dir)
        list_file_in_dir(path, file_path_list,suffix)

    file_path_list.sort()
    return file_path_list




def GetFileSize(dir_list):
    max_size = 0
    max_file = ""
    for filePath in dir_list:
        fsize = os.path.getsize(filePath)
        fsize = fsize / float(1024 * 1024)

        if max_size < fsize:
            max_size = fsize
            max_file = filePath
    print("max = ", max_file, max_size)



def FileType(file):
    import chardet
    encode_type = chardet.detect(open(file, 'rb').read())["encoding"]
    # print("encode_type =",encode_type)

    if encode_type !=None:
        if "utf" not in encode_type and "UTF" not in encode_type:
            encode_type = "GBK"
    return encode_type

def list_file_in_dir(path, list_name,suffix):
    # print(path)
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            list_file_in_dir(file_path, list_name,suffix)
        else:
            if suffix!=None:
                if file_name.endswith(suffix):
                    list_name.append(file_path)
            else:
                list_name.append(file_path)




def get_file_list(data_root_path, suffix=None,only_name=False):
    file_paths_list = []
    filelist = sorted(os.listdir(data_root_path))
    for idx, file_name in enumerate(filelist):

        if suffix is not None :
            if file_name.endswith(suffix):
                if only_name==False:
                    file_path = os.path.join(data_root_path, file_name)
                else:
                    file_path = file_name
    
                file_paths_list.append(file_path)
        else:

            if only_name == False:
                file_path = os.path.join(data_root_path, file_name)
            else:
                file_path = file_name
            file_paths_list.append(file_path)

    return file_paths_list


def get_file_list_append(data_root_path,file_paths_list, suffix=None, only_name=False):
    filelist = sorted(os.listdir(data_root_path))
    for idx, file_name in enumerate(filelist):

        if suffix is not None:
            if file_name.endswith(suffix):
                if only_name == False:
                    file_path = os.path.join(data_root_path, file_name)
                else:
                    file_path = file_name

                file_paths_list.append(file_path)
        else:

            if only_name == False:
                file_path = os.path.join(data_root_path, file_name)
            else:
                file_path = file_name
            file_paths_list.append(file_path)

    return file_paths_list


def copy_file(srcfile, dstfile):
    import shutil
    shutil.copyfile(srcfile, dstfile)

def move_file(srcfile, dstfile):
    import shutil
    shutil.move(srcfile, dstfile)

def copy_files_in_dir(src_path,dst_path):
    dst_file_num = len(get_file_list(dst_path))
    print("dst_path num = ",dst_file_num)


    from tqdm import tqdm
    file_name_list = get_file_list(src_path)
    print("src_path num = ",len(file_name_list))

    for idx in tqdm(range(len(file_name_list)),desc="copy: "):
        img_name = file_name_list[idx]
        src_file = os.path.join(src_path,img_name)
        dst_file = os.path.join(dst_path,img_name)
        copy_file(src_file,dst_file)
    
    dst_plus_src_num = dst_file_num + len(file_name_list)
    
    print("dst_plus_src_num ",dst_plus_src_num)
    print("res dst_path num = ",len(get_file_list(dst_path)))

    
def copy_files_main():
    img_path = ""
    dst_path=""

    file_name_list = get_file_list(img_path,".png",only_name=True)
    for idx,img_name in (enumerate(file_name_list)):
        if idx>100:
            break

        src_file = os.path.join(img_path,img_name)
        dst_file = os.path.join(dst_path,img_name)
        crazylib.copy_file(src_file,dst_file)

