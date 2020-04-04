from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import joblib
import csv
import os
import sys

path = os.path.abspath(os.path.dirname(sys.argv[0]))
feature = []
result_f = []
result_t = []
data_file = csv.reader(open(path + '/data/train.csv'))
for content in data_file:
    content = list(map(float, content))
    if len(content) != 0:
        feature.append(content[0:13])
        result_f.append(content[14])
        result_t.append(content[15])
scaler = StandardScaler()
scaler.fit(feature)
feature = scaler.transform(feature)
feature_train_f, feature_test_f, result_train_f, result_test_f = \
    train_test_split(feature, result_f, test_size=0.2, random_state=1)

feature_train_t, feature_test_t, result_train_t, result_test_t = \
    train_test_split(feature, result_t, test_size=0.2, random_state=1)

clf_f = RandomForestRegressor()
clf_t = RandomForestRegressor()
clf_f.fit(feature_train_f, result_train_f)
clf_t.fit(feature_train_t, result_train_t)
predict_result_f = clf_f.predict(feature_test_f)
predict_result_t = clf_t.predict(feature_test_t)
print(accuracy_score(predict_result_f, result_test_f))
print(accuracy_score(predict_result_t, result_test_t))
print(classification_report(predict_result_f, result_test_f))
print(classification_report(predict_result_t, result_test_t))
joblib.dump(clf_f, path + "/model/model_f.pkl")
joblib.dump(clf_t, path + "/model/model_t.pkl")
