import os
from tools import file_io as fio


cam_name = 'Cam72'
class_name = fio.class_dir_1
dir_list = [fio.train_dir, cam_name, class_name]
test_path = fio.createPath(fio.sep, dir_list, '')


try:
    print(test_path)
    with open(test_path, 'r', encoding='utf-8') as f:
        print('successful')
except:
    print('failing')