import pandas as pd
import xgboost as xgb
import numpy as np


features = pd.read_csv('sub_9_fdelay.csv', delimiter=',')

# itd['itd'] = itd['itd'].apply(lambda x: abs(x))

bst = xgb.Booster(model_file='delay_final.model')
dpred = xgb.DMatrix(features)
result = bst.predict(dpred)

result_df = pd.DataFrame(data=result.reshape(-1,1), columns=['est_itd'])
result_df_full = pd.concat([result_df, features.loc[0:1249]['azi'],
                           features.loc[0:1249]['ele']], axis=1)
result_df_full.to_csv('sub_9_delay.csv', index=False)


# result_df.to_csv('xgb_result.csv', index=False)


# for plotting
'''
import matplotlib.pyplot as plt
plt.scatter(features['d7_r'].iloc[14:17], result_df.iloc[14:17])
plt.title("d7_r")
'''


