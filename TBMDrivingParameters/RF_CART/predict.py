import joblib
import csv
import os
import sys

path = os.path.abspath(os.path.dirname(sys.argv[0]))
data = []
result_f = []
result_t = []
data_file = csv.reader(open(path + '/data/predict.csv'))
for content in data_file:
    content = list(map(float, content))
    if len(content) != 0:
        data.append(content)
clf_f = joblib.load(path + '/model/model_f.pkl')
clf_t = joblib.load(path + '/model/model_t.pkl')
print(clf_f.predict(data))
print(clf_t.predict(data))
