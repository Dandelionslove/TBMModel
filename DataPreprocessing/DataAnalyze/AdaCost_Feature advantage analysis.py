from sklearn.ensemble import RandomForestClassifier
import csv

Y = []
X = []
names=[]
with open('allIndexAdaCost.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    result = list(reader)
    result[0].pop(193)
    names = result[0]

    for i in range(1, len(result)):
        for j in range(0, len(result[i])):
            if(result[i][j]!=''):
                result[i][j]= float(result[i][j])
        Y.append(result[i].pop(193))
        X.append(result[i])

rf = RandomForestClassifier(n_estimators=200)

rf.fit(X, Y)

print("Features sorted by their score:")

print(sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), reverse=True))