import pandas
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from AdaCost import AdaCostClassifier
from sklearn.model_selection import KFold
import pickle
import os
import sys

path = os.path.abspath(os.path.dirname(sys.argv[0]))
df = pandas.read_csv(path + '/data/adaCostPreData.csv', encoding='utf-8', index_col=False)
X = df[['刀盘运行时间均值', '撑靴压力均值', '刀盘转速均值', '撑靴泵压力均值', '左撑靴俯仰角均值', '控制泵压力均值', '右撑靴俯仰角均值',
        '左撑靴滚动角均值', '左撑靴油缸行程检测均值', '右撑靴滚动角均值', '右撑靴油缸行程检测均值']].values
y = df['围岩等级'].values

cost_matrix = [[0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 4, 2, 1],
               [0, 0, 1, 0, 2, 1],
               [0, 0, 2, 4, 0, 1],
               [0, 0, 2, 6, 4, 0]]

kf = KFold(n_splits=10)
# train_error = []
# test_error = []
adaCost = None

train_accuracy_with_n_est = []
test_accuracy_with_n_est = []

for n_est in range(1, 200):
    test_accuracy = 0.0
    train_accuracy = 0.0
    for train_index, test_index in kf.split(X):
        adaCost = AdaCostClassifier(
            DecisionTreeClassifier(max_depth=5),
            n_estimators=n_est,
            learning_rate=0.1,
            algorithm="SAMME",
            cost_matrix=cost_matrix
            )
        # print('X_train:%s ' % X[train_index])
        # print('X_test: %s ' % X[test_index])
        adaCost.fit(X[train_index], y[train_index])
        test_accuracy += accuracy_score(y[test_index], adaCost.predict(X[test_index])) / 10.0
        train_accuracy += accuracy_score(y[train_index], adaCost.predict(X[train_index])) / 10.0
        # test_error.append(1.0 - accuracy_score(y[test_index], adaCost.predict(X[test_index])))
        # train_error.append(1.0 - accuracy_score(y[train_index], adaCost.predict(X[train_index])))
    test_accuracy_with_n_est.append(test_accuracy)
    train_accuracy_with_n_est.append((train_accuracy))
    print('n_est: ', n_est)
    print('train', train_accuracy)
    print('test', test_accuracy)
        # for discrete_train_predict in adaCost.staged_predict(X[train_index]):
        #     print(1. - accuracy_score(discrete_train_predict, y[train_index]))


# print(path)
s = pickle.dumps(adaCost)
f = open(path + '/model/adaCost.pickle', 'wb+')
f.write(s)
f.close()

axis = [i for i in range(1, 200)]
l1, = plt.plot(axis, train_accuracy_with_n_est, color='red', linewidth=2.0, label='train accuracy')
l2, = plt.plot(axis, test_accuracy_with_n_est, color='blue', linewidth=3.0, label='test accuracy')
plt.xlabel('number of estimator')
plt.ylabel('accuracy')
plt.legend([l1, l2], ['train accuracy', 'test accuracy'])
plt.savefig(path + '/image/train.png')
plt.show()
