import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras import regularizers
print(tf.__version__)

import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from tools import file_io as fio


rgb_dir_list = [fio.proj_dir, fio.train_dir]
rgb_name = 'final_data.csv'
rgb_dir = fio.createPath(fio.sep, rgb_dir_list, rgb_name)


rgb_dp = pd.read_csv(rgb_dir)
dataset = pd.DataFrame(rgb_dp)
print('RGB CSV data columns: ')
print(dataset.columns)
print('RGB CSV data shape: ' + str(dataset.shape))


#   Converting Categorical Data of 'label` into Numerical
dataset.label.unique()
dataset = pd.get_dummies(dataset, columns=['label'])
print('Converted RGB CSV data columns: ')
print(dataset.columns)
print('Converted RGB CSV data shape: ' + str(dataset.shape))


#   Data Correlation
f, ax = plt.subplots(figsize=(15, 9))
corr = dataset.corr()
hm = sns.heatmap(round(corr,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f', linewidths=.05)
f.subplots_adjust(top=0.93)
t= f.suptitle('Correlation Heatmap', fontsize=15)


#   Split the data into train and test¶
train_dataset = dataset.sample(frac=0.8, random_state=8)    # train = 80%,  random_state = any int value means every time when you run your program you will get the same output for train and test dataset, random_state is None by default which means every time when you run your program you will get different output because of splitting between train and test varies within
test_dataset = dataset.drop(train_dataset.index)    # remove train_dataset from dataframe to get test_dataset
print('Training data columns: ')
print(train_dataset.columns)
print('Training data shape: ' + str(train_dataset.shape))
print('Testing data columns: ')
print(test_dataset.columns)
print('Testing data shape: ' + str(test_dataset.shape))


#   Split features: rgb and labels
train_labels = pd.DataFrame([train_dataset.pop(x) for x in ['label_white', 'label_black']]).T
print('Training label columns: ')
print(train_labels.columns)
print('Training label shape: ' + str(train_labels.shape))
test_labels = pd.DataFrame([test_dataset.pop(x) for x in ['label_white', 'label_black']]).T
print('Testing label columns: ')
print(test_labels.columns)
print('Testing label shape: ' + str(test_labels.shape))


#   Build and Compile Models
model = keras.Sequential([
    layers.Dense(3, kernel_regularizer=regularizers.l2(0.001), activation='relu', input_shape=[len(train_dataset.keys())]), #inputshape=[3]
    layers.Dense(24, kernel_regularizer=regularizers.l2(0.001), activation='relu'),
    layers.Dense(24, kernel_regularizer=regularizers.l2(0.001), activation='relu'),
    layers.Dense(16, kernel_regularizer=regularizers.l2(0.001), activation='relu'),
    layers.Dense(2)
  ])

optimizer = keras.optimizers.Adam(learning_rate=0.001)
loss_function = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
model.compile(loss=loss_function, optimizer=optimizer, metrics=['accuracy'])
print('Model Summary: ')
model.summary()

history = model.fit(x=train_dataset, y=train_labels,
                    validation_split=0.2,
                    epochs=5001,
                    batch_size=2048,
                    verbose=0,
                    callbacks=[tfdocs.modeling.EpochDots()],
                    shuffle=True)

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()

plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)
plotter.plot({'Basic': history}, metric = "accuracy")
plt.ylim([0, 1])
plt.ylabel('accuracy [Color]')

plotter.plot({'Basic': history}, metric = "loss")
plt.ylim([0, 1])
plt.ylabel('loss [Color]')

model.save('clsf_model.h5')