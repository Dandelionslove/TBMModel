import pandas
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_recall_fscore_support
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
adaCost = None

train_accuracy_with_n_est = []
test_accuracy_with_n_est = []
recall_with_n_est = []
f1_with_n_est = []
class_recall_with_n_est = [[], [], [], []]
# model_pkl = None
for n_est in range(1, 200):
    test_accuracy = 0.0
    train_accuracy = 0.0
    recall = 0.0
    f1 = 0.0
    class_recall = []
    # print("n_est", n_est)
    for train_index, test_index in kf.split(X):
        adaCost = AdaCostClassifier(
            DecisionTreeClassifier(max_depth=5),
            n_estimators=n_est,
            learning_rate=0.1,
            algorithm="SAMME",
            cost_matrix=cost_matrix
            )
        adaCost.fit(X[train_index], y[train_index])
        # print(accuracy_score(y, adaCost.predict(X)))
        true = y[test_index]
        pred = adaCost.predict(X[test_index])
        test_accuracy += accuracy_score(true, pred) / 10.0
        train_accuracy += accuracy_score(y[train_index], adaCost.predict(X[train_index])) / 10.0
        f1 += f1_score(true, pred, average='macro') / 10.00
        recall += recall_score(true, pred, average='macro') / 10.00
        # print(y[test_index])
        # print(adaCost.predict(X[test_index]))
        p_class, r_class, f_class, support_micro = precision_recall_fscore_support(y_true=true,
                                                                                   y_pred=pred,
                                                                            labels=[2, 3, 4, 5], average=None)
        class_recall.append(r_class)

    for class_n in range(4):
        count = 0
        sum = 0.0
        for fold in class_recall:
            if fold[class_n] == 0: continue
            count += 1
            sum += fold[class_n]
        if count == 0:
            class_recall_with_n_est[class_n].append(0)
        else:
            class_recall_with_n_est[class_n].append(sum / count)

    test_accuracy_with_n_est.append(test_accuracy)
    train_accuracy_with_n_est.append(train_accuracy)
    recall_with_n_est.append(recall)
    f1_with_n_est.append(f1)


s = pickle.dumps(adaCost)
f = open(path + '/model/adaCost.pickle', 'wb+')
f.write(s)
f.close()

# print(train_accuracy_with_n_est)
# print(test_accuracy_with_n_est)
# print(recall_with_n_est)
# print(f1_with_n_est)
axis = [i for i in range(1, 200)]

plt.figure(1)
# 将第一个画板划分为2行1列组成的区块，并获取到第一块区域
ax1 = plt.subplot(211)
plt.xlabel('number of estimator')
plt.ylabel('percentage')
l1, = plt.plot(axis, train_accuracy_with_n_est, color='red', linewidth=2.0, label='train accuracy')
l2, = plt.plot(axis, test_accuracy_with_n_est, color='blue', linewidth=3.0, label='test accuracy')
l3, = plt.plot(axis, recall_with_n_est, color='green', linewidth=2.0, label='test recall')
l4, = plt.plot(axis, f1_with_n_est, color='yellow', linewidth=3.0, label='test f1')
plt.legend([l1, l2, l3, l4], ['train accuracy', 'test accuracy', 'test recall', 'test f1'])
ax2 = plt.subplot(212)
plt.xlabel('number of estimator')
plt.ylabel('percentage')
l1, = plt.plot(axis, class_recall_with_n_est[0], color='red', linewidth=2.0, label='class 2')
l2, = plt.plot(axis, class_recall_with_n_est[1], color='blue', linewidth=3.0, label='class 3')
l3, = plt.plot(axis, class_recall_with_n_est[2], color='green', linewidth=2.0, label='class 4')
l4, = plt.plot(axis, class_recall_with_n_est[3], color='yellow', linewidth=3.0, label='class 5')
plt.legend([l1, l2, l3, l4], ['class 2', 'class 3', 'class 4', 'class 5'])
plt.savefig(path + '/image/train.png')
plt.show()
