import pandas
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_recall_fscore_support
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
import pickle
import os
import sys
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from imblearn.over_sampling import RandomOverSampler,SMOTE, ADASYN

path = os.path.abspath(os.path.dirname(sys.argv[0]))
df = pandas.read_csv(path + '/adaCostPreData.csv', encoding='utf-8', index_col=False)
X = df[['刀盘运行时间均值', '撑靴压力均值', '刀盘转速均值', '撑靴泵压力均值', '左撑靴俯仰角均值', '控制泵压力均值', '右撑靴俯仰角均值',
        '左撑靴滚动角均值', '左撑靴油缸行程检测均值', '右撑靴滚动角均值', '右撑靴油缸行程检测均值']].values
y = df['围岩等级'].values


# 十折交叉验证
kf = KFold(n_splits=10)

ros = RandomOverSampler(random_state=0)
#X, y = ros.fit_sample(X, y)
X, y = SMOTE().fit_sample(X, y)
# X, y = ADASYN().fit_sample(X, y)


# 记录每次迭代的数据
train_accuracy_with_n_est = []  # 随弱分类器个数的训练准确率
test_accuracy_with_n_est = []  # 随弱分类器个数的测试准确率
recall_with_n_est = []  # 随弱分类器个数的召回率
f1_with_n_est = []  # 随弱分类器个数的f1
class_recall_with_n_est = [[], [], [], []] # 随弱分类器个数的每个类的召回率

adaCost = None
n_est_range = range(55, 65)
for n_est in n_est_range:
    test_accuracy = 0.0
    train_accuracy = 0.0
    recall = 0.0
    f1 = 0.0
    class_recall = []
    print("使用", n_est, "个弱分类器：")
    for train_index, test_index in kf.split(X):
        adaCost = AdaBoostClassifier(
            DecisionTreeClassifier(max_depth=10),
            n_estimators=n_est,
            learning_rate=0.1,
            # algorithm="SAMME",
            # cost_matrix=cost_matrix
            )
        # adaCost.fit(X[train_index], y[train_index],sample_weight[train_index])
        adaCost.fit(X[train_index], y[train_index])
        truth = y[test_index]
        pred = adaCost.predict(X[test_index])

        # 准确率 召回率 f1-score 分类召回率
        test_accuracy += accuracy_score(truth, pred) / 10.0
        train_accuracy += accuracy_score(y[train_index], adaCost.predict(X[train_index])) / 10.0
        f1 += f1_score(truth, pred, average='macro') / 10.00
        recall += recall_score(truth, pred, average='macro') / 10.00
        p_class, r_class, f_class, support_micro = precision_recall_fscore_support(
            y_true=truth, y_pred=pred, labels=[2, 3, 4, 5], average=None)
        class_recall.append(r_class)

    # 计算各类的平均召回率，如果该类没有出现，不考虑计入平均值
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


def log(result_list):
    result_str = ''
    for i in range(len(result_list)):
        result_str += str(i + 1)
        result_str += '个弱分类器： '
        result_str += str(result_list[i])
        result_str += '\n'
    result_str += '最佳：'
    result_str += str(max(result_list))
    return result_str


def log2(result_list):
    result_str = ''
    for class_i in range(len(result_list)):
        result_str += 'class'
        result_str += str(class_i + 2)
        result_str += '\n'
        for i in range(len(result_list[class_i])):
            result_str += str(i + 1)
            result_str += '个弱分类器： '
            result_str += str(result_list[class_i][i])
            result_str += '\n'
        result_str += '最佳：'
        result_str += str(max(result_list[class_i]))
        result_str += '\n'
    return result_str


# 保存模型
file = open(path + '/model/adaCost.pickle', 'wb+')
pickle.dump(adaCost, file)
# 各个指标写入文件
file = open(path + '/image/test_accuracy_with_n_est.txt','w')
# result_str = ''
file.write(log(test_accuracy_with_n_est))
file.close()
file = open(path + '/image/train_accuracy_with_n_est.txt','w')
file.write(log(train_accuracy_with_n_est))
file.close()
file = open(path + '/image/recall_with_n_est.txt','w')
file.write(log(recall_with_n_est))
file.close()
file = open(path + '/image/f1_with_n_est.txt','w')
file.write(log(f1_with_n_est))
file.close()
file = open(path + '/image/class_recall_with_n_est.txt','w')
file.write(log2(class_recall_with_n_est))
file.close()




