import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
import tensorflow.keras.backend as K

cipic = pd.read_csv('feature_cipic.csv', delimiter=',')
feature = pd.read_csv('./sub_9_fann.csv', delimiter=',')


def datascale(train, test):
    scaler = MinMaxScaler()
    scaler.fit(train)
    train_norm = scaler.transform(train)
    test_norm = scaler.transform(test)
    return train_norm, test_norm


features_train_norm, features_test_norm = datascale(cipic, feature)


tf.keras.backend.clear_session()

Inputs = keras.Input(shape=(features_train_norm.shape[1],), dtype=tf.float32, name='feature')

x = keras.layers.Dense(64, activation=tf.nn.relu, dtype=tf.float32)(Inputs)
x = keras.layers.Dense(128, activation=tf.nn.relu, dtype=tf.float32)(x)
x = keras.layers.Dense(256, activation=tf.nn.relu, dtype=tf.float32)(x)
x = keras.layers.Dense(256, activation=tf.nn.relu, dtype=tf.float32)(x)
x = keras.layers.Dense(128, activation=tf.nn.relu, dtype=tf.float32)(x)
outputs = keras.layers.Dense(200, dtype=tf.float32)(x)

model = keras.Model(inputs=Inputs, outputs=outputs)

model.compile(optimizer=tf.train.AdamOptimizer(0.000001),  # adam0.005
              loss='mse')

model.load_weights('./ann_final_3/checkpoints')

result = model.predict(features_test_norm)

result = result*2
hrir_result = pd.DataFrame(data=result)
hrir_result_full = pd.concat([hrir_result, feature.azi, feature.ele], axis=1)
hrir_result_full.to_csv('hrir_sub_9.csv', index=False)

'''
#for correlartion plor
import matplotlib.pyplot as plt
for i in range(128, 134):
    plt.plot(result[i])
    plt.title("theta2 at 0 0 ")
'''
