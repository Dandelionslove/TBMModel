import pandas
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from AdaCost import AdaCostClassifier
from sklearn.model_selection import KFold
import pickle

df = pandas.read_csv(r"C:\Users\chend\Desktop\Book1.csv", encoding='utf-8', index_col=False)
X = df[['dim1', 'dim2', 'dim3']].values
y = df['y'].values

cost_matrix = [[0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 4, 2, 1],
               [0, 0, 1, 0, 2, 1],
               [0, 0, 2, 4, 0, 1],
               [0, 0, 2, 6, 4, 0]]

kf = KFold(n_splits=10) # 十折交叉验证
train_error = []
test_error = []
adaCost = None
for train_index, test_index in kf.split(X):
    adaCost = AdaCostClassifier(
        DecisionTreeClassifier(max_depth=5),
        n_estimators=100,
        learning_rate=1.5,
        algorithm="SAMME",
        cost_matrix=cost_matrix)
    # print('X_train:%s ' % X[train_index])
    # print('X_test: %s ' % X[test_index])
    adaCost.fit(X[train_index], y[train_index])
    test_error.append(1.0 - accuracy_score(y[test_index], adaCost.predict(X[test_index])))
    train_error.append(1.0 - accuracy_score(y[train_index], adaCost.predict(X[train_index])))
    for discrete_train_predict in adaCost.staged_predict(X[train_index]):
        print(1. - accuracy_score(discrete_train_predict, y[train_index]))

s = pickle.dumps(adaCost)
f = open('adaCost.txt', 'wb+')
f.write(s)
f.close()

axis = [i + 1 for i in range(10)]
plt.plot(axis, train_error, color='red', linewidth=2.0, label='train error')
plt.plot(axis, test_error, color='blue', linewidth=3.0, label='test error')
plt.xlabel('cross validation times')
plt.ylabel('error rate')
plt.show()
