from sklearn.ensemble import RandomForestClassifier
# 随即森林分类器，回归器使用RandomForestRegressor
import csv
# csv文件 用于存储原始数据
from sklearn.model_selection import train_test_split
# 将原始数据按照比例分割为“测试集”和“训练集”
from sklearn.metrics import accuracy_score
# 分类准确率分数
from sklearn.metrics import confusion_matrix
# 混淆矩阵
from sklearn.metrics import classification_report
# 显示主要分类指标的文本报告．在报告中显示每个类的精确度，召回率，F1值等信息。
from sklearn.preprocessing import StandardScaler
# 对特征数据进行归一化

data = []
traffic_feature = []
traffic_target = []
csv_file = csv.reader(
    open('/Users/shizi9/Desktop/STLab/code/packSize_all.csv'))
# csv.reader()返回一个reader对象，利用该对象遍历csv文件中的行
# open('sample\\student.csv') as f:
# row = csv.reader(f, delimiter = ',')
# next(row)  #去掉第一行定义：id name height。。。等
for content in csv_file:
    # content指file中的每一行
    content = list(map(float, content))
    # map在python3中返回的是迭代器，需要转化成map格式
    # 批量处理 将内容转化为float
    if len(content) != 0:
        data.append(content)
        # 读取字段
        traffic_feature.append(content[0:6])
        # 0到6行是feature
        traffic_target.append(content[-1])
        # 列表中的最后一个元素 是分类
print('data=', data)
print('traffic_feature=', traffic_feature)
print('traffic_target=', traffic_target)
scaler = StandardScaler()
# 标准化转换
scaler.fit(traffic_feature)
# 训练标准化对象
traffic_feature = scaler.transform(traffic_feature)
# 转换数据集
feature_train, feature_test, target_train, target_test = train_test_split(
    traffic_feature, traffic_target, test_size=0.3, random_state=0)
# 将数据分为训练集和测试集
clf = RandomForestClassifier()
clf.fit(feature_train, target_train)
# 计算森林
predict_results = clf.predict(feature_test)
# 预测分类
print(accuracy_score(predict_results, target_test))
conf_mat = confusion_matrix(target_test, predict_results)
print(conf_mat)
print(classification_report(target_test, predict_results))