from sklearn.ensemble import RandomForestRegressor
import csv

Y = []
X = []
names=[]
with open('allIndexRF.csv', 'r', encoding='utf-8') as f:

    reader = csv.reader(f)
    result = list(reader)

    result[0].pop(196)
    result[0].pop(195)
    for i in range(1, len(result)):
        for j in range(0, len(result[i])):
            if(result[i][j]!=''):
                result[i][j]= float(result[i][j])
        Y.append(result[i].pop(196))
        result[i].pop(195)
        X.append(result[i])
    names=result[0]


rf = RandomForestRegressor(n_estimators=200)

rf.fit(X, Y)

print("Features sorted by their score:")

print(sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), reverse=True))