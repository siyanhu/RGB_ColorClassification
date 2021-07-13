import pandas as pd
from tools import file_io as fio


rgb_dir_list = [fio.proj_dir, fio.rgb_dir]
rgb_dir = fio.createPath(fio.sep, rgb_dir_list)
rgb_raw_files = fio.traverse_dir(rgb_dir, full_path=True)

rslt = list()
for i in range(len(rgb_raw_files)):
    file_path = rgb_raw_files[i]
    dp = pd.read_csv(file_path)
    df = pd.DataFrame(dp)
    file_mark = 'white'
    if 'black' in file_path:
        file_mark = 'black'
    for index, row in df.iterrows():
        r_value = df.loc[index, 'r']
        g_value = df.loc[index, 'g']
        b_value = df.loc[index, 'b']
        rgb_dict = {'red': r_value,	'green': g_value, 'blue': b_value, 'label': file_mark}
        if (rgb_dict in rslt) == False:
            if index % 1000 == 0:
                print('no. ' + str(index) + ', ' + str(rgb_dict))
            rslt.append((rgb_dict))

rgb_df = pd.DataFrame(rslt)
save_dir_list = [fio.proj_dir, fio.train_dir]
save_name = 'final_data.csv'
save_dir = fio.createPath(fio.sep, save_dir_list, save_name)
fio.save_df_to_csv(rgb_df, save_dir, write_header=True)
