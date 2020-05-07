import pandas as pd
import tensorflow as tf
import sklearn as sk
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow import keras
import function
import tensorflow.keras.backend as K

df = pd.read_csv('hrir_combined_bypeak.csv', delimiter=',')
fea = pd.read_csv('feature_combined.csv', delimiter=',')
#df = df.drop(['Unnamed: 0'], axis=1)
fea = fea.drop(['Unnamed: 0'], axis=1)
fea = fea.drop(['sex', 'age', 'weight'], axis=1)

features_train, features_test, label_train, label_test = function.split_sub(fea, df, 3)
label_test = label_test.drop(['azi', 'ele'], axis=1)
label_train = label_train.drop(['azi', 'ele'], axis=1)



features_train_norm, features_test_norm = function.datascale(features_train, features_test)
label_test = label_test/2
label_train = label_train/2

tf.keras.backend.clear_session()

Inputs = keras.Input(shape=(features_train_norm.shape[1],), dtype=tf.float32, name='feature')

x = keras.layers.Dense(64, activation=tf.nn.relu, dtype=tf.float32)(Inputs)
x = keras.layers.Dense(128, activation=tf.nn.relu, dtype=tf.float32)(x)
x = keras.layers.Dense(256, activation=tf.nn.relu, dtype=tf.float32)(x)
x = keras.layers.Dense(256, activation=tf.nn.relu, dtype=tf.float32)(x)
x = keras.layers.Dense(128, activation=tf.nn.relu, dtype=tf.float32)(x)
outputs = keras.layers.Dense(200, dtype=tf.float32)(x)

model = keras.Model(inputs=Inputs, outputs=outputs)


model.compile(optimizer=tf.train.AdamOptimizer(0.0005, 0.9, 0.999, epsilon=1e-07),  # adam0.005, 0.000001
              loss='mse')
callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0,
                                                    patience=0, verbose=0, mode='auto')

history = model.fit(features_train_norm,
                    label_train,
                    epochs=400,
                    validation_split=0.2,
                    callbacks=[callback])

function.plot_history(history)

model.save_weights('./ann_final/checkpoints')
model = build_model()
model.load_weights('./ann_final/checkpoints')

result = model.predict(features_test_norm)
result = result*2
ev = sk.metrics.mean_squared_error(label_test, result)

for i in range(0, 10, 2):
    print(i)
    fg = plt.plot(label_test.iloc[i])
    fg = plt.plot(result[i])
    plt.show(fg)
    plt.clf()

