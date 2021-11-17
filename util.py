import os
def guarantee_path_exists(path):
    if "/" in path:
        paths = path.split("/")
        # print(paths)
        path_num = len(paths)
        current_path = ''
        for i in range(path_num):
            if len(paths[i]) > 0:
                if paths[i][0] == ".":
                    current_path = current_path + paths[i] + "/"
                else:
                    current_path = current_path + paths[i] + "/"
                    if not os.path.exists(current_path):
                        os.mkdir(current_path)
    else:
        os.mkdir(path)

def getFileList(input_folder, suffix):
    raw_files = []
    # 读input_path下所有的suffix文件名
    for file in os.listdir(input_folder):
        file_path = os.path.join(file)
        if os.path.splitext(file_path)[1] == suffix:
            raw_files.append(file_path)
    return raw_files