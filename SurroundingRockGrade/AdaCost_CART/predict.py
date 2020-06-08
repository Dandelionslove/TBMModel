import pickle
import os
import sys


def adaCost(sample):
    # 可以接受（样本数X特征数）这样的二维ndarray，也可以接受只有一个样本的一维数组（会自动转换为只有一行的二维数组）
    # 输出一个一维list，第i个元素（数字）代表第i个样本预测的围岩等级。
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    f = open(path + '/model/adaCost.pickle', 'rb')
    s = f.read()
    model = pickle.loads(s)
    if len(sample.shape) == 1:
        sample = sample.reshape(1, len(sample))
    return model.predict(sample).tolist()
