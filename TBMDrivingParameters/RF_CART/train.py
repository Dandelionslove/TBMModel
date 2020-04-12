from sklearn.ensemble import RandomForestRegressor
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
# import matplotlib.pyplot as plt

path = os.path.abspath(os.path.dirname(sys.argv[0]))
feature = []
result_f = []
result_t = []
data_file = csv.reader(open(path + '/data/train.csv'))
next(data_file)
for content in data_file:
    content = list(map(float, content))
    if len(content) != 0:
        feature.append(content[1:15])
        result_f.append(content[16])
        result_t.append(content[15])
scaler = StandardScaler()
scaler.fit(feature)
feature = scaler.transform(feature)
feature_train_f, feature_test_f, result_train_f, result_test_f = \
    train_test_split(feature, result_f, test_size=0.2, random_state=0)

feature_train_t, feature_test_t, result_train_t, result_test_t = \
    train_test_split(feature, result_t, test_size=0.2, random_state=0)

# scores_f = []
# for i in range(500, 1000, 10):
#     rf = RandomForestRegressor(n_estimators=50, oob_score=True, min_samples_split=3, min_samples_leaf=2)
#     rf.fit(feature_train_f, result_train_f)
#     predict_result_f = rf.predict(feature_test_f)
#     score = r2_score(predict_result_f, result_test_f)
#     scores_f.append(score)
# print(max(scores_f))
# plt.plot(range(500, 1000, 10), scores_f)
# plt.show()

# scores_t = []
# for i in range(500, 1000, 10):
#     rf = RandomForestRegressor(n_estimators=50, oob_score=True, min_samples_split=3, min_samples_leaf=1)
#     rf.fit(feature_train_t, result_train_t)
#     predict_result_t = rf.predict(feature_test_t)
#     score = r2_score(predict_result_t, result_test_t)
#     scores_t.append(score)
# print(max(scores_t))
# plt.plot(range(500, 1000, 10), scores_t)
# plt.show()

clf_f = RandomForestRegressor(n_estimators=50,
                              n_jobs=-1,
                              oob_score=True,
                              min_samples_split=3,
                              min_samples_leaf=2)
clf_t = RandomForestRegressor(n_estimators=50,
                              n_jobs=-1,
                              oob_score=True,
                              min_samples_split=3,
                              min_samples_leaf=1)
clf_f.fit(feature_train_f, result_train_f)
clf_t.fit(feature_train_t, result_train_t)
predict_result_f = clf_f.predict(feature_test_f)
predict_result_t = clf_t.predict(feature_test_t)
log_file = open((path + '/log.txt'), mode='w')
log_file.write('explained_variance_score of F: ' +
               str(explained_variance_score(predict_result_f, result_test_f)) +
               '\n')
log_file.write('explained_variance_score of T: ' +
               str(explained_variance_score(predict_result_t, result_test_t)) +
               '\n')
log_file.write('mean_squared_error of F: ' +
               str(mean_squared_error(predict_result_f, result_test_f)) + '\n')
log_file.write('mean_squared_error of T: ' +
               str(mean_squared_error(predict_result_t, result_test_t)) + '\n')
log_file.write('mean_squared_log_error of F: ' +
               str(mean_squared_log_error(predict_result_f, result_test_f)) +
               '\n')
log_file.write('mean_squared_log_error of T: ' +
               str(mean_squared_log_error(predict_result_t, result_test_t)) +
               '\n')
log_file.write('median_absolute_error of F: ' +
               str(median_absolute_error(predict_result_f, result_test_f)) +
               '\n')
log_file.write('median_absolute_error of T: ' +
               str(median_absolute_error(predict_result_t, result_test_t)) +
               '\n')
log_file.write('mean_absolute_error of F: ' +
               str(mean_absolute_error(predict_result_f, result_test_f)) +
               '\n')
log_file.write('mean_absolute_error of T: ' +
               str(mean_absolute_error(predict_result_t, result_test_t)) +
               '\n')
log_file.write('r2_score of T: ' +
               str(r2_score(predict_result_f, result_test_f)) + '\n')
log_file.write('r2_score of T: ' +
               str(r2_score(predict_result_t, result_test_t)) + '\n')
log_file.close()
joblib.dump(clf_f, path + "/model/model_f.pkl")
joblib.dump(clf_t, path + "/model/model_t.pkl")
