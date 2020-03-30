import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


class RF:
    def __init__(self):
        # Address为存放txt文件夹相对于DataPreprocessing.py的路径
        self.Address = '../TBMData'
        # RFIndex为RF需要使用数据的列索引，即参数名称
        self.RFIndex = ['总推进力', '刀盘功率', '刀盘扭矩', '推进速度', '刀盘速度给定', '刀盘转速']
        self.result = {}
        self.resultList = []
        self.dataList = AllTxtHandle(self.Address, self.RFIndex)

    def RFData(self):
        for data in self.dataList:
            torque = data['刀盘扭矩'].values

            number = 0
            while number < len(torque) - 31:
                # 判断是否为上升段，并选取前30个数据
                if torque[number] == 0 and torque[number + 1] > 0 and torque[number + 30] > 0:
                    for name in self.RFIndex:
                        self.calculateRise(data, name, number)

                    # 判断稳定段，并选取稳定段数据
                    self.calculateStable(data['刀盘转速'].values, number + 31, '稳定段刀盘转速均值')
                    self.calculateStable(data['推进速度'].values, number + 31, '稳定段推进速度均值')

                    self.resultList.append(self.result)

                    number = number + 31

                else:
                    number = number + 1
        # print(self.resultList)
        return self.resultList

    # 判断稳定段，并选取稳定段数据
    def calculateStable(self, data, figture, name):
        # 判断稳定段起点
        if figture < len(data) - 1:
            while data[figture + 1] - data[figture] > 0:
                if figture + 1 == len(data):
                    break
                figture = figture + 1

        stableData = []
        # 判断稳定段终点，并选取稳定段数据
        while figture < len(data):
            stableData.append(data[figture])
            if np.var(stableData) > 5:
                stableData.remove(data[figture])
                self.result[name] = np.mean(stableData)
                break
            elif figture + 1 == len(data):
                self.result[name] = np.mean(stableData)
            figture = figture + 1

    # 判断上升段，并选取上升段数据
    def calculateRise(self, data, name, number):
        info = data[name].values
        info = info[number + 1:number + 31]
        mean = info.mean()
        var = info.var()
        self.result[name + '均值'] = mean
        self.result[name + '方差'] = var


# AdaCostIndex为adacost需要使用数据的列索引，即参数名称
AdaCostIndex = ['刀盘转速电位器值', '刀盘运行时间', '撑靴压力', '刀盘转速', '撑靴泵压力', '左撑靴俯仰角', '控制泵压力', '右撑靴俯仰角', '撑靴滚动角', '撑靴油缸行程检测']


# 调用该函数处理文件夹下所有txt文件，dirAddress为相对DataPreprocessing.py的路径，index为需要使用数据的列索引，即参数名称
def AllTxtHandle(dirAddress, index):
    # 因为python的相对路径默认为相对运行文件的路径，所以转为绝对路径
    address = transAddress(dirAddress)
    data = []
    for root, dirs, files in os.walk(address):
        for file in files:
            path = os.path.join(root, file)
            oneTxtData = oneTxtHandle(path, index)
            data.append(oneTxtData)

    return data


# 调用该函数读取单个txt文件数据，oneDataAddress为相对DataPreprocessing.py的路径，index为需要使用数据的列索引，即参数名称
def oneTxtHandle(oneDataAddress, index):
    # 因为python的相对路径默认为相对运行文件的路径，所以转为绝对路径
    address = transAddress(oneDataAddress)
    # 读入数据
    basicData = pd.read_table(address)
    # 选取需要的列组成DataFrame
    frame = pd.DataFrame(basicData, columns=index)
    # 删除缺失行：当行中有任意一个值为缺失时，删除行
    data_del_lack_row = frame.dropna()
    # 处理误差
    oneTxtData = errorHandle(data_del_lack_row, index)

    return oneTxtData


# 处理误差
def errorHandle(data, index):
    # 行索引列表
    rowIndex = data.index
    # 待删除的行索引列表
    toDel = []
    # 循环每一列
    for columnName in index:
        # 获取该列数据
        oneColumn = data[columnName]
        # 计算该列平均值
        mean = oneColumn.mean()
        # 计算该列标准差
        sigma = oneColumn.std()
        # 判断是否单个数据与平均值差的绝对值大于三倍的标准差，是则记录该行
        for info in range(len(oneColumn)):
            # 记录该行索引值
            if (oneColumn.values[info] - mean) > (3 * sigma) or (mean - oneColumn.values[info]) > (3 * sigma):
                if rowIndex[info] not in toDel:
                    toDel.append(rowIndex[info])
    # 删除所有记录行
    data.drop(toDel, inplace=True)

    return data


# 将相对路径转绝对路径
def transAddress(relativePath):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    absolutePath = os.path.normpath(os.path.join(base_dir, relativePath))
    return absolutePath

# def adaCostData():
#     global AdaCostIndex, Address
#     data = AllTxtHandle(Address, AdaCostIndex)
#     for info in data:
#         for index in AdaCostIndex:
#             mean = data[index].mean
# rf = RF()
# rf.RFData()
