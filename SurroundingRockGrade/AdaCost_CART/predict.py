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


f = open('adaCost.txt', 'rb')
s = f.read()
adaCost = pickle.loads(s)

print(adaCost.predict(X[1]))