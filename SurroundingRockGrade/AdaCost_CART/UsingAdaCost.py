import pandas as pd
import numpy as np
from sklearn.datasets import make_gaussian_quantiles
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from AdaCost import AdaCostClassifier


def read_file(filename):
    # 读取文件并且选择一些列作为特征
    df = pd.read_csv(filename, sep='\t', encoding='utf-8', index_col=False)
    X = np.array(df[['刀盘转速电位器设定值', '刀盘运行时间', '撑靴压力']])
    y = np.array(df['围岩级别']) # 应该整合两个表格后才有这个列
    return X, y

X, y = read_file(r"C:\Users\chend\Desktop\CREC188_20150710.txt")


n_split = 3000

X_train, X_test = X[:n_split], X[n_split:]
y_train, y_test = y[:n_split], y[n_split:]

adaCost = AdaCostClassifier(
    DecisionTreeClassifier(max_depth=10),
    n_estimators=100,
    learning_rate=1.5,
    algorithm="SAMME")

adaCost.fit(X_train, y_train)

test_errors = []

for discrete_train_predict in adaCost.staged_predict(X_test):
    test_errors.append(
        1. - accuracy_score(discrete_train_predict, y_test))

n_trees = len(adaCost)

# Boosting might terminate early, but the following arrays are always
# n_estimators long. We crop them to the actual number of trees here:
estimator_errors = adaCost.estimator_errors_[:n_trees]
estimator_weights = adaCost.estimator_weights_[:n_trees]

plt.figure(figsize=(15, 5))

plt.subplot(131)
plt.plot(range(1, n_trees + 1),
         test_errors, c='black')
plt.ylabel('Test Error')
plt.xlabel('Number of Trees')


# plt.subplot(132)
# plt.plot(range(1, n_trees + 1), estimator_errors,
#          "b", alpha=.5)
# plt.legend()
# plt.ylabel('Error')
# plt.xlabel('Number of Trees')


# plt.subplot(133)
# plt.plot(range(1, n_trees + 1), estimator_weights,
#          "b")
# plt.legend()
# plt.ylabel('Weight')
# plt.xlabel('Number of Trees')


# prevent overlapping y-axis labels
plt.subplots_adjust(wspace=0.25)
plt.show()

