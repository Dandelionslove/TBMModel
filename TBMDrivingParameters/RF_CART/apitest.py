import csv
import os
import sys
from sklearn.preprocessing import StandardScaler
from predict import RF_CART


path = os.path.abspath(os.path.dirname(sys.argv[0]))
# data is input parameter
data = []
# read data from a csv file
data_file = csv.reader(open(path + '/data/predict.csv'))
for content in data_file:
    content = list(map(float, content))
    if len(content) != 0:
        data.append(content)
scaler = StandardScaler()
scaler.fit(data)
data = scaler.transform(data)
# call function RF_CART
[result_t, result_f] = RF_CART(data)
print(result_t)
print(result_f)