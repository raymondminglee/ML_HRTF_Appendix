import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.decomposition import PCA
import math


def split_sub(features, hrir, sub_id):
    features_train = features.loc[features['subject_id'] != sub_id]
    features_test = features.loc[features['subject_id'] == sub_id]
    label_train = hrir.loc[hrir['subject_id'] != sub_id]
    label_test = hrir.loc[hrir['subject_id'] == sub_id]
    features_train = features_train.drop(['subject_id'], axis=1)
    features_test = features_test.drop(['subject_id'], axis=1)
    label_train = label_train.drop(['subject_id'], axis=1)
    label_test = label_test.drop(['subject_id'], axis=1)
    return features_train, features_test, label_train, label_test


def get_angle(azi, ele, features_train, features_test, label_train, label_test):
    y_train = label_train.loc[label_train['azi'] == azi]
    x_train = features_train.loc[features_train['azi'] == azi]
    y_test = label_test.loc[label_test['azi'] == azi]
    x_test = features_test.loc[features_test['azi'] == azi]


    y_train = y_train.loc[y_train['ele'] == ele]
    x_train = x_train.loc[x_train['ele'] == ele]
    y_test = y_test.loc[y_test['ele'] == ele]
    x_test = x_test.loc[x_test['ele'] == ele]

    x_train = x_train.drop(['azi'], axis=1)
    y_train = y_train.drop(['azi', 'ele'], axis=1)
    x_test = x_test.drop(['azi'], axis=1)
    y_test = y_test.drop(['azi', 'ele'], axis=1)
    return x_train, x_test, y_train, y_test

def plot_history(history):
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('loss')
    plt.plot(history.epoch, np.array(history.history['loss']),
             label='Train Loss')
    plt.plot(history.epoch, np.array(history.history['val_loss']),
             label='Val loss')
    plt.legend()
    # plt.ylim([0, 0.005])


def datascale(train, test):
    scaler = MinMaxScaler()
    scaler.fit(train)
    train_norm = scaler.transform(train)
    test_norm = scaler.transform(test)
    return train_norm, test_norm


def pcatest(y_train_norm):
    pca_test = PCA(n_components=30)
    pca_test.fit(y_train_norm)
    total = 0
    for ee, evr in enumerate(pca_test.explained_variance_ratio_):
        total = total + evr
        if total < 0.90:
            n_com = ee + 1
    n_com = n_com + 1
    return n_com

def build_model(data, n_com):
    model = keras.Sequential([
        keras.layers.Dense(32, activation=tf.nn.relu,
                           input_shape=(data.shape[1],)),
        keras.layers.Dense(64, activation=tf.nn.relu),
        keras.layers.Dense(32, activation=tf.nn.relu),
        # keras.layers.Dense(256, activation=tf.nn.relu),
        # keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(n_com)
    ])

    optimizer = tf.train.RMSPropOptimizer(0.001)
    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mse'])
    return model


def rmse(data_true, data2):
    error = math.sqrt((sum(data2-data_true)**2)/200)
    return error
