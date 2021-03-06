from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.metrics import explained_variance_score
from sklearn.preprocessing import StandardScaler
import joblib
import csv
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

path = os.path.abspath(os.path.dirname(sys.argv[0]))
feature = []
result_f = []
result_t = []
data_file = pd.read_csv((path + '/data/train.csv'), sep=',', engine='python')
result_t = data_file['稳定段刀盘扭矩均值'].values
result_f = data_file['稳定段总推进力均值'].values
data_file = data_file.values
for i in range(len(data_file)):
    content = list(map(float, data_file[i]))
    feature.append(content[1:15])
# for content in data_file:
#     content = list(map(float, content))
#     if len(content) != 0:
#         feature.append(content[1:15])
#         result_t.append(content[15])
#         result_f.append(content[16])
scaler = StandardScaler()
scaler.fit(feature)
feature = scaler.transform(feature)
feature_train_t, feature_test_t, result_train_t, result_test_t = \
    train_test_split(feature, result_t, test_size=0.1, random_state=0)

feature_train_f, feature_test_f, result_train_f, result_test_f = \
    train_test_split(feature, result_f, test_size=0.1, random_state=0)

# param = {
#     'loss': ['ls', 'lad', 'huber', 'quantile'],
#     'n_estimators':
#     range(50, 150, 10),
#     'max_depth':
#     range(2, 20, 1),
#     'max_features':
#     range(7, 14, 1),
# }

# gcv_t = GridSearchCV(estimator=GradientBoostingRegressor(),
#                      param_grid=param,
#                      cv=2)
# gcv_t.fit(feature, result_t)

# joblib.dump(gcv_t, path + "/model/model_t.pkl")

# log_file = open((path + '/log.txt'), mode='w')
# log_file.write('best_score of T: ' + str(gcv_t.best_score_) + '\n')
# log_file.write('best_params of T: ' + str(gcv_t.best_params_) + '\n')

clf_t = GradientBoostingRegressor(loss='huber', max_depth=5, max_features=10, n_estimators=100)
clf_f = GradientBoostingRegressor(loss='huber', max_depth=6, max_features=8, n_estimators=120)
clf_t.fit(feature_train_t, result_train_t)
clf_f.fit(feature_train_f, result_train_f)
predict_result_t = clf_t.predict(feature_test_t)
predict_result_f = clf_f.predict(feature_test_f)

log_file = open((path + '/log1.txt'), mode='w')
log_file.write('explained_variance_score of T: ' +
               str(explained_variance_score(predict_result_t, result_test_t)) +
               '\n')
log_file.write('explained_variance_score of F: ' +
               str(explained_variance_score(predict_result_f, result_test_f)) +
               '\n')
log_file.write('mean_squared_error of T: ' +
               str(mean_squared_error(predict_result_t, result_test_t)) + '\n')
log_file.write('mean_squared_error of F: ' +
               str(mean_squared_error(predict_result_f, result_test_f)) + '\n')
log_file.write('mean_squared_log_error of T: ' +
               str(mean_squared_log_error(predict_result_t, result_test_t)) +
               '\n')
log_file.write('mean_squared_log_error of F: ' +
               str(mean_squared_log_error(predict_result_f, result_test_f)) +
               '\n')
log_file.write('median_absolute_error of T: ' +
               str(median_absolute_error(predict_result_t, result_test_t)) +
               '\n')
log_file.write('median_absolute_error of F: ' +
               str(median_absolute_error(predict_result_f, result_test_f)) +
               '\n')
log_file.write('mean_absolute_error of T: ' +
               str(mean_absolute_error(predict_result_t, result_test_t)) +
               '\n')
log_file.write('mean_absolute_error of F: ' +
               str(mean_absolute_error(predict_result_f, result_test_f)) +
               '\n')
log_file.write('r2_score of T: ' +
               str(r2_score(predict_result_t, result_test_t)) + '\n')
log_file.write('r2_score of F: ' +
               str(r2_score(predict_result_f, result_test_f)) + '\n')
log_file.write('importances of T: ' + str(clf_t.feature_importances_) + '\n')
log_file.write('importances of F: ' + str(clf_f.feature_importances_) + '\n')
log_file.write('cross_val_score of F: ' +
               str(cross_val_score(clf_t, feature, result_t)) + '\n')
log_file.write('cross_val_score of F: ' +
               str(cross_val_score(clf_f, feature, result_f)) + '\n')
log_file.close()
joblib.dump(clf_t, path + "/model/model_t.pkl")
joblib.dump(clf_f, path + "/model/model_f.pkl")
