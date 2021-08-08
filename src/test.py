import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
print(tf.__version__)

import PIL
import cv2
from PIL import Image

import tools.file_io as fio
from tools import time_tool as ttol


cam_name = 'Cam72'
time_mark = '20210714_1'
test_dir_list = [fio.proj_dir, fio.test_dir, cam_name]
test_dir = fio.createPath(fio.sep, test_dir_list)

# self-define ground_truth
# test_dir = '/home/siyanhu/smartlight/train/Cam72/2'
# gt = 'white'
# gt_value = '2'

img_paths = fio.traverse_dir(test_dir, full_path=True)

save_dir_list = [fio.proj_dir, fio.pred_dir, time_mark]


model = tf.keras.models.load_model('clsf_model_1.h5')
#model = tf.keras.models.load_model('clsf_model-500.hdf5')


def find_highest_freq_element_from_list(list_value):
    #maxlabel = max(list_value, key = list_value.count)
    maxlabel = max(list_value)
    return maxlabel


def get_rgb_midpoint(image, i, j):
    width, height = image.size
    if i > width or j > height:
        return image.getpixel((i / 2, j / 2))
    pixel = image.getpixel((i, j))
    return pixel

def get_rgb_histfeature(image_path):
    image = cv2.imread(image_path)
    chans = cv2.split(image)
    colors = ('b', 'g', 'r')
    features = []
    counter = 0
    for (chan, color) in zip(chans, colors):
        counter = counter + 1
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        features.extend(hist)
        # find the peak pixel values for R, G, and B
        elem = np.argmax(hist)
        if counter == 1:
            blue = elem
        elif counter == 2:
            green = elem
        elif counter == 3:
            red = elem
    rslt = (red, green, blue)
    return rslt


def get_rgb_histogram(image):
    r, g, b = image.split()
    l1 = r.histogram()
    l2 = g.histogram()
    l3 = b.histogram()
    rslt = (find_highest_freq_element_from_list(l1), find_highest_freq_element_from_list(l2), find_highest_freq_element_from_list(l3))
    return rslt


def get_rgb(image_path, image, i, j):
    return get_rgb_histfeature(image_path)
    #   return get_rgb_histogram(image)
    #   return get_rgb_midpoint(image, i, j)


def output_color_vector(img_path, width_scale, height_scale):
    img = Image.open(img_path)
    width, height = img.size
    rgb = get_rgb(img_path, img, width_scale, height_scale)
    input = np.reshape(rgb, (-1, 3))  # reshaping as per input to ANN model
    return input


def get_img_info(img_path):
    img_name = fio.get_filename_from_path(img_path, with_filetype=False)
    if len(img_name) == 0:
        return img_name
    elif ('_' in img_name) == False:
        return img_name
    else:
        parts = img_name.split('_')
        return parts


save_rslt = list()
for i in range(len(img_paths)):
    #   label_white = 1
    #   label_black = 2
    before_timer = ttol.current_timestamp(False)
    path = img_paths[i]
    img_info = get_img_info(path)
    if len(img_info) < 2:
        continue
    ts = img_info[0]
    ptid = img_info[1]
    input_rgb = output_color_vector(path, 5, 5)
    color_class_confidence = model.predict_proba(input_rgb)  # Output of layer is in terms of Confidence of the 11 classes
    if len(color_class_confidence) < 0:
        continue
    confidence_list = color_class_confidence[0]
    if len(confidence_list) < 2:
        continue
    black_conf = confidence_list[1]
    white_conf = confidence_list[0]
    pred_rslt = '1'
    pred_conf = black_conf
    if white_conf > black_conf:
        pred_rslt = '2'
        pred_conf = white_conf
    after_timer = ttol.current_timestamp(False)
    duration = after_timer - before_timer
    save_rslt.append({'Timestamp': ts, 'Patch': ptid, 'Prediction': pred_rslt, 'confidence': pred_conf, 'runtime': duration})
    if (i % 500 == 0) and (i > 0):
        pred_df = pd.DataFrame(save_rslt)
        csv_name = cam_name + '_' + time_mark + '_' + str(i) + '.csv'
        save_path = fio.createPath(fio.sep, save_dir_list, csv_name)
        fio.save_df_to_csv(pred_df, save_path, write_header=True, mode='a+', encode='utf_8_sig', breakline='')
        print('saving predict result: ' + save_path)
        save_rslt = list()


if len(save_rslt) > 0:
    pred_df = pd.DataFrame(save_rslt)
    print(pred_df.columns)
    csv_name = cam_name + '_' + time_mark + '_' + str(i) + '.csv'
    save_path = fio.createPath(fio.sep, save_dir_list, csv_name)
    fio.save_df_to_csv(pred_df, save_path, write_header=True)
    print('saving predict result: ' + save_path)