import pandas as pd
import xgboost as xgb
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import sklearn as sk


features = pd.read_csv('./xgbmodel/perdataclean.csv', delimiter=',')
itd = pd.read_csv('./xgbmodel/itd_clean.csv', delimiter=',')

# itd['itd'] = itd['itd'].apply(lambda x: abs(x))

sub_id = 3


def split_sub():
    feature_train = features.loc[features['subject_id'] != sub_id]
    feature_test = features.loc[features['subject_id'] == sub_id]
    label_train = itd.loc[itd['subject_id'] != sub_id]
    label_test = itd.loc[itd['subject_id'] == sub_id]
    feature_train = feature_train.drop(['subject_id', 'weight', 'age', 'sex'], axis=1)
    feature_test = feature_test.drop(['subject_id', 'weight', 'age', 'sex'], axis=1)
    label_train = label_train.drop(['subject_id', 'azi', 'ele'], axis=1)
    label_test = label_test.drop(['subject_id', 'azi', 'ele'], axis=1)
    # label_train = label_train.drop(['subject_id'], axis=1)
    # label_test = label_test.drop(['subject_id'], axis=1)
    return feature_train, feature_test, label_train, label_test


features_train, features_test, label_train, label_test = split_sub()
X_train, X_test, Y_train, Y_test = split_sub()
# X_train, X_test, Y_train, Y_test = get_angle(-45, 0, features_train, features_test, label_train, label_test)
X_train_train, X_train_test, Y_train_train, Y_train_test = train_test_split(X_train, Y_train, test_size=0.1)

dtrain = xgb.DMatrix(X_train_train, label=Y_train_train)
dtest = xgb.DMatrix(X_train_test, label=Y_train_test)
evallist = [(dtest, 'eval'), (dtrain, 'train')]


param_final = {'max_depth': 7, 'eta': 0.001, 'silent':0, 'objective': 'reg:linear',
               'colsample_bylevel': 1, 'min_child_weight': 10, 'subsample': 0.2, 'colsample_bytree': 1,
               'colsample_bynode': 0.2, 'gamma': 5, 'nthread': 4, 'eval_metric': 'rmse', 'lambda': 0.001, 'tree_method': 'exact'}
num_train = 20000
bst = xgb.train(param_final, dtrain, num_train, evallist, early_stopping_rounds=10)
# bst.save_model('xgb_51.model')


dpred = xgb.DMatrix(X_test)
result = bst.predict(dpred)

bst.save_model('delay_final.model')

# bst = xgb.Booster(model_file='xgb.model')

bst = xgb.Booster(model_file='delay_final.model')
dpred = xgb.DMatrix(X_test)
result = bst.predict(dpred)
EV = sk.metrics.mean_squared_error(Y_test, result)

result_df = pd.DataFrame(data=result.reshape(-1,1), columns=['est_itd'])
result_df_full = pd.concat([result_df, features.loc[0:1249]['subject_id'], features.loc[0:1249]['azi'],
                           features.loc[0:1249]['ele']], axis=1)
result_df_full.to_csv('delay_result_sub135.csv', index=False)

