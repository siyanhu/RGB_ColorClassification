import sys
import tools.file_io as fio
import pandas as pd

cam_name = 'Cam72'
time_mark = '20210713_2'
csv_dir = [fio.proj_dir, fio.pred_dir, time_mark]
file_name = 'Cam72.csv'
score_path = fio.createPath(fio.sep, csv_dir, file_name)


score_dp = pd.read_csv(score_path)
score_df = pd.DataFrame(score_dp)
print(score_df.columns)

def equal(a, b):
    a = int(a)
    b = int(b)
    if a == b:
        return 1
    else:
        return 0


score_df['accuracy'] = score_df .apply(lambda x : equal(x['Prediction'],x['Color (Ground-Truth)']),axis = 1)
score_0 = len(score_df[score_df['accuracy'] == 0].Timestamp)
score_1 = len(score_df[score_df['accuracy'] == 1].Timestamp)
print('Among ' + str(score_0 + score_1) + ' predictions, ' + str(score_1) + ' items are accurate. So the accuracy rate is ' + str(float(score_1/(score_0 + score_1))))


file_name = 'Cam72_score.csv'
file_path = fio.createPath(fio.sep, csv_dir, file_name)
fio.save_df_to_csv(score_df, file_path, write_header=True)