


def print_list(data_list,max_n=-1):
    for idx,data in enumerate(data_list):
        if idx>max_n and max_n>0:
            break
        print(data)