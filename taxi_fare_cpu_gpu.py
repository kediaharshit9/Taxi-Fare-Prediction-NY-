# -*- coding: utf-8 -*-
"""cloud_test3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HDwAHql7osAikUtPtZLRyoqHKT2GdL9P
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

from __future__ import print_function
import pandas as pd
import datetime as dt
from sklearn import metrics
import tensorflow as tf
import numpy as np
import math
from tensorflow.python.data import Dataset
from sklearn.model_selection import train_test_split
import tensorflow.losses as loss_utils
from sklearn.preprocessing import LabelEncoder
import math

data_set = pd.read_csv('/content/drive/My Drive/Ass4_data/train.csv', sep = ',', nrows = 100000);


data_set.fillna(method='bfill',inplace=True)

time = pd.to_datetime(data_set['pickup_datetime'], format="%Y-%m-%d %H:%M:%S UTC", exact = True)
#data_set['year'] = [i.year for i in time]
data_set['month'] = [i.month for i in time]
data_set['date'] = [i.day for i in time]
data_set['hour'] = [i.hour for i in time]
data_set['minute'] = [i.minute for i in time]

input = data_set.to_numpy()
input = input[np.all(input != 0, axis=1)]
input[:, 3] += 73
input[:, 4] -= 40
input[:, 5] += 73
input[:, 6] -= 40

x_train,x_test,y_train,y_test = train_test_split(input[:, 3:],input[:, 1],shuffle=True,test_size=0.1)

x_train = x_train.astype('float32')
y_train = y_train.astype('float32')
x_test = x_test.astype('float32')
y_test = y_test.astype('float32')

print(x_train.shape,x_test.shape,y_train.shape,y_test.shape)

def init_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, 0.01, 0.01))

def init_biases(shape):
    return tf.Variable(tf.zeros(shape))

def fully_connected_layer(inputs, input_shape, output_shape, activation=tf.nn.relu):

    weights = init_weights([input_shape, output_shape])
    biases = init_biases([output_shape])
    
    layer = tf.matmul(inputs, weights) + biases
    
    if activation != None:
        layer = activation(layer)
        
    return layer

inputs =  tf.placeholder(tf.float32, [None, 9], name='Inputs')
targets =  tf.placeholder(tf.float32, [None, 1], name='Targets')

#defining the network
l1 = fully_connected_layer(inputs, 9, 10)
l2 = fully_connected_layer(l1, 10, 10)
l3 = fully_connected_layer(l2, 10, 10)
l4 = fully_connected_layer(l3, 10, 1, activation=None)
predictions = l4

cost = loss2 = tf.reduce_mean(tf.squared_difference(targets, predictions))
learning_rate = 0.001
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

epochs = 1000
batch_size = 1000

from tqdm import tqdm

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    #TRAINING PORTION OF THE SESSION
    for i in tqdm(range(epochs)):
        idx = np.random.choice(len(x_train), batch_size, replace=True)
        x_batch = x_train[idx, :]
        y_batch = y_train[idx]
        y_batch = np.reshape(y_batch, (len(y_batch), 1))
        
        batch_loss, opt = sess.run([cost, optimizer], feed_dict={inputs:x_batch, targets:y_batch})
        
        if i % 100 == 0:
            print("error: " , batch_loss)
    
    #TESTING PORTION OF THE SESSION
    preds = sess.run([predictions], feed_dict={inputs:x_test})
    preds = np.reshape(preds, (len(y_test)))
    print(max(preds), min(preds))

rmse = 0
for i in range(len(preds)):
    rmse += (preds[i] - y_test[i])**2
rmse /= len(preds)
print(rmse**0.5)

preds

