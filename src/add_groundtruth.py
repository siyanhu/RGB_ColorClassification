import sys
import tools.file_io as fio
import pandas as pd


cam_name = 'Cam72'
time_mark = '20210713_1'
csv_list = [fio.proj_dir, fio.pred_dir, time_mark]
csv_dir = fio.createPath(fio.sep, csv_list)
csv_paths = fio.traverse_dir(csv_dir, full_path=True)


pred_file_paths = list()
gt_file_path = ''

for filepath in csv_paths:
    if (time_mark in filepath) == False:
        continue
    if '.zip' in filepath:
        continue
    elif  ('.csv' in filepath) and (fio.gtr_dir in filepath):
        gt_file_path = filepath
        continue
    elif ('.csv' in filepath) and (('GroundTruth' in filepath) == False):
        pred_file_paths.append(filepath)


if len(gt_file_path) == 0:
    print('No ground truth file found.')
    sys.exit(0)
gt_dp = pd.read_csv(gt_file_path)
gt_df = pd.DataFrame(gt_dp)
#gt_df.rename(columns={'Timestamp':  'timstamp', 'Patch': 'patch'}, inplace=True)
print(gt_df.columns)


file_name = cam_name + '.csv'
for i in range(len(pred_file_paths)):
    filepath = pred_file_paths[i]
    pred_dp = pd.read_csv(filepath)
    pred_df = pd.DataFrame(pred_dp)
    if i == 0:
        print('pred_df columns: ')
        print(pred_df.columns)
    intersected_df = pd.merge(pred_df, gt_df, on=['Timestamp', 'Patch'], how='inner')
    print('intersected dataframe shape: ' + str(intersected_df.shape))
    intersected_df['Color (Ground-Truth)'] = '0'
    print('Intersected dataframe: ')
    print(filepath)
    print(intersected_df.columns)
    intersected_df.loc[intersected_df['Ground_Truth'] == 'Black', ['Color (Ground-Truth)']] = '1'
    intersected_df.loc[intersected_df['Ground_Truth'] == 'Natural', ['Color (Ground-Truth)']] = '2'
    dir_list = [fio.proj_dir, fio.pred_dir, time_mark]
    save_path = fio.createPath(fio.sep, dir_list, file_name)
    add_header_to_csv = False
    if i == 0:
        add_header_to_csv = True
    fio.save_df_to_csv(intersected_df, save_path, write_header=add_header_to_csv)
    print('done: ' + filepath)
