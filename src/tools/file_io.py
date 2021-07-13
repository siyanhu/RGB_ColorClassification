import time
import datetime
import csv
import os

proj_dir = 'D:\\Gits\\RGB_ColorClassification\\data'
#proj_dir = '//home//siyanhu//smartlight'


sep = os.sep
train_dir = 'train'
test_dir = 'test'
pred_dir = 'pred'
anno_dir = 'Annotations'
img_dir = 'cam_imgs'
class_dir_1 = '1'
class_dir_2 = '2'
temp_dir = 'temp'
gtr_dir = 'GroundTruth'
rgb_dir = 'rgb'


def createPath(separator, list_of_dir, file_name=""):
    if len(list_of_dir) <= 0:
        return ""
    while '' in list_of_dir:
        list_of_dir.remove('')
    path_rslt = separator.join(list_of_dir)
    if len(file_name) <= 0:
        return path_rslt
    else:
        return path_rslt + separator + file_name


def traverse_dir(dir, full_path=False):
    rslt = list()
    g = os.walk(dir)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            if full_path:
                rslt.append(os.path.join(path, file_name))
            else:
                rslt.append(file_name)
    return rslt


def getFilePathFromDir(dir, file_type='csv', sep=sep):
    files = os.listdir(dir)
    if len(file_type) <= 0:
        return files
    rslt = list()
    for file in files:
        components = file.split('.')
        len_comp = len(components)
        if len_comp <= 0:
            continue
        type_component = components[len_comp - 1]
        if type_component == file_type:
            path = createPath(sep, [dir], file)
            rslt.append(path)
    return rslt


def string2timestamp(ts_str, ts_format):
#     "%Y-%m-%d %H:%M:%S.%f"
    d = datetime.datetime.strptime(ts_str, ts_format)
    t = d.timetuple()
    timeStamp = int(time.mktime(t))
    return timeStamp


def split_path(file_path):
    return os.path.split((file_path))


def get_filename_from_path(file_path, with_filetype=True):
    components = split_path(file_path)
    if len(file_path) < 1:
        return ''
    full_name = components[-1]
    if with_filetype:
        return full_name
    elif ('.' in full_name) == False:
        return full_name
    else:
        name_parts = full_name.split('.')
        return name_parts[0]



def save_df_to_csv(rslt_df, file_path, write_header=False, mode='a+', encode='utf_8_sig', breakline=''):

    header = list(rslt_df.head())
    with open(file_path, mode, encoding=encode, newline=breakline) as f:
        writer = csv.writer(f)
        header = list(rslt_df.head())
        if write_header:
            writer.writerow(header)
        for index, row in rslt_df.iterrows():
            writer.writerow(row)
        f.close()


def save_dict_to_csv(dict_to_save, file_path, mode='a', encode='utf_8_sig', breakline=''):
    keyword_list = dict_to_save.keys()
    try:
        # 第一次打开文件时，第一行写入表头
        if not os.path.exists(file_path):
            with open(file_path, "w", newline='', encoding='utf-8') as csvfile:  # newline='' 去除空白行
                writer = csv.DictWriter(csvfile, fieldnames=keyword_list)  # 写字典的方法
                writer.writeheader()  # 写表头的方法

        # 接下来追加写入内容
        with open(file_path, mode=mode, newline=breakline, encoding=encode) as csvfile:  # newline='' 一定要写，否则写入数据有空白行
            writer = csv.DictWriter(csvfile, fieldnames=keyword_list)
            writer.writerow(dict_to_save)  # 按行写入数据

    except Exception as e:
        print("write error==>", e)
        pass
    
    
def save_str_to_txt(str_to_save, file_path, mode='a', encode='utf_8_sig', breakline=''):
    try:
        if not os.path.exists(file_path):
            with open(file_path, "w", newline='', encoding='utf-8') as f:  # newline='' 去除空白行
                f.write(str_to_save)                
        else:
            with open(file_path, mode=mode, newline=breakline, encoding=encode) as f:
                f.write(str_to_save)
    except Exception as e:
        print("write error==>", e)
        pass


def create_folder(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        print('Folder existed: ' + dir_path)


def delete_file(path):
    if os.path.exists(path):  # 如果文件存在
        os.remove(path)
    else:
        print('no such file:%s' % path)


def rename_file(oldname, newname):
    os.rename(oldname, newname)