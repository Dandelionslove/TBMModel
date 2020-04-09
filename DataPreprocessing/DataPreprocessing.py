import matplotlib
import pandas as pd
import os
import numpy as np
import zipfile
import matplotlib.pyplot as plt

# 相对路径均为相对DataPreprocessing.py的路径
# 存放txt数据的文件夹
txtAddress = '../../txtData'
# 存放预处理数据的文件夹
preDataAddress = '../../TBMPreproData'
# 存放zip压缩包的文件夹
zipAddress = '../../Data'
# 围岩等级表地址
rockFormAddress = '../TBMData/围岩等级信息统计表-现场工程师统计.xlsx'
# 存放可视化图片
picDirAddress = '../../DataPic'


class RF:
    def __init__(self):
        #存放预处理数据地址
        self.dataPath = '../TBMDrivingParameters/RF_CART/data'
        # 预处理数据文件名
        self.DataFileName = 'train.csv'
        # Address为存放txt文件夹相对于DataPreprocessing.py的路径
        self.Address = txtAddress
        # RFIndex为RF需要使用数据的列索引，即参数名称
        self.RFIndex = ['总推进力', '刀盘功率', '刀盘扭矩', '推进速度', '刀盘速度给定', '刀盘转速']
        # RFStableIndex为稳定段所需数据的列索引
        self.RFStableIndex = ['刀盘转速', '推进速度', '刀盘扭矩', '总推进力']
        self.resultList = []
        # 处理原始数据的缺失和误差
        self.dataDict = AllTxtHandle(self.Address, self.RFIndex)

    def RFData(self):
        for date in self.dataDict:
            data = self.dataDict[date]
            torque = data['刀盘扭矩'].values
            speed = data['推进速度'].values
            f = data['总推进力'].values

            # plot根据列表绘制出有意义的图形
            plt.plot(torque, color='blue', label='T')
            plt.plot(f, color='green', label='F')
            plt.plot(speed, color='red', label='S')
            plt.legend()
            # 设置图标标题
            plt.title(date, fontsize=24)
            # 设置坐标轴标签
            plt.xlabel("time/s")
            plt.ylabel("")
            # plt.xlim(23000, 24500)
            # 设置刻度标记的大小
            plt.tick_params(axis='both', labelsize=14)
            # 转绝对地址
            picDirPath = transAddress(picDirAddress)
            # 不存在则创建
            if not os.path.exists(picDirPath):
                os.makedirs(picDirPath)
            # 预处理文件路径
            picFilePath = os.path.join(picDirPath, date[0:-4] + '.png')
            #生成图片
            plt.savefig(picFilePath)
            #清空缓存
            plt.close()
            # 打开matplotlib查看器，并显示绘制图形
            # plt.show()

            # print(np.mean(torque))
            # print(len(torque) - 31)
            number = 0
            while number < len(torque) - 31:
                # 判断是否为上升段，并选取前30个数据
                if torque[number] == torque[number + 1] and torque[number] != 0 \
                        and torque[number + 2] - torque[number + 1] > 2 and torque[number + 30] > 0 \
                        and torque[number + 2] - torque[number + 1] > 0:
                    #上升段起点为number + 2
                    number = number + 2
                    result = self.calculateRise(data, number)

                    # 判断稳定段起点
                    number = number + 31
                    if number < len(torque) - 1:
                        while torque[number + 1] - torque[number] > 0:
                            if number + 1 == len(torque):
                                break
                            number = number + 1

                    stableData = []
                    end = number
                    # 通过刀盘扭矩列表方差大于5时， 判断稳定段终点， 并选取稳定段数据
                    while end < len(torque):
                        stableData.append(torque[end])
                        if np.var(stableData) > 5:
                            end = end - 1
                            for index in self.RFStableIndex:
                                result['稳定段' + index + '均值'] = calculateStable(number, data[index].values, end)
                            break
                        elif end + 1 == len(torque):
                            for index in self.RFStableIndex:
                                result['稳定段' + index + '均值'] = calculateStable(number, data[index].values, end)
                            break
                        else:
                            end = end + 1
                    # 将单个循环段数据放入数据列表中
                    number = end + 1

                    flag = 1

                    for i in result:
                        if result[i] == 0:
                            flag = 0
                            break

                    if flag:
                        self.resultList.append(result)
                    # print(result)

                else:
                    number = number + 1
        # print(self.resultList)
        df = pd.DataFrame(self.resultList)
        # print(df)
        # 生成预处理数文件
        createPreproData(df, self.dataPath, self.DataFileName)


        return df

    # 判断上升段，并选取上升段数据
    def calculateRise(self, data, number):
        result = {}
        for name in self.RFIndex:
            info = data[name].values
            info = info[number + 1:number + 31]
            mean = info.mean()
            var = info.var()
            result[name + '均值'] = mean
            result[name + '方差'] = var

        return result


class AdaCost:
    def __init__(self):
        # 预处理数据文件名
        self.DataFileName = 'adaCostPreData.csv'
        # AdaCostIndex为adacost需要使用数据的列索引，即参数名称，额外加入刀盘扭矩判断上升段与稳定段
        self.AdaCostIndex = ['桩号', '刀盘运行时间', '撑靴压力', '刀盘扭矩', '刀盘转速', '撑靴泵压力', '左撑靴俯仰角', '控制泵压力',
                             '右撑靴俯仰角', '左撑靴滚动角', '左撑靴油缸行程检测', '右撑靴滚动角',
                             '右撑靴油缸行程检测']#, '刀盘转速电位器值设定值'
        # Address为存放txt文件夹相对于DataPreprocessing.py的路径
        self.Address = txtAddress

        self.dataDict = AllTxtHandle(self.Address, self.AdaCostIndex)
        self.resultList = []
        # 围岩映射表处理
        self.rockForm = pd.read_excel(transAddress(rockFormAddress))
        self.rockOrigin = self.rockForm['起始桩号']
        self.rockEnd = self.rockForm['结束桩号']
        self.rockGrade = self.rockForm['修正围岩等级']

    def adaCostData(self):
        for date in self.dataDict:
            data = self.dataDict[date]
            torque = data['刀盘扭矩'].values
            number = 0
            while number < len(torque) - 31:
                # 判断上升段起点
                if torque[number] == torque[number + 1] and torque[number] != 0 \
                        and torque[number + 2] - torque[number + 1] > 2 and torque[number + 30] > 0 \
                        and torque[number + 2] - torque[number + 1] > 0:
                    # 判断稳定段起点
                    number = number + 31
                    if number < len(torque) - 1:
                        while torque[number + 1] - torque[number] > 0:
                            if number + 1 == len(torque):
                                break
                            number = number + 1

                    stableData = []
                    result = {}
                    end = number
                    # 通过刀盘扭矩列表方差大于5时， 判断稳定段终点， 并选取稳定段数据
                    while end < len(torque):
                        stableData.append(torque[end])
                        if np.var(stableData) > 5:
                            end = end - 1
                            for name in self.AdaCostIndex:
                                if name != '刀盘扭矩' and name != '桩号':
                                    result[name + '均值'] = calculateStable(number, data[name].values, end)
                                    result['围岩等级'] = self.calRockGrade(data['桩号'].values[number: end + 1])
                            break
                        elif end + 1 == len(torque):
                            for name in self.AdaCostIndex:
                                if name != '刀盘扭矩' and name != '桩号':
                                    result[name + '均值'] = calculateStable(number, data[name].values, end)
                                    result['围岩等级'] = self.calRockGrade(data['桩号'].values[number: end + 1])
                            break
                        else:
                            end = end + 1
                    self.resultList.append(result)
                    # print(result)
                    number = end + 1
                else:
                    number = number + 1

        # print(self.resultList)
        df = pd.DataFrame(self.resultList)
        print(df)
        # 生成预处理数据文件
        createPreproData(df, preDataAddress, self.DataFileName)
        return df

    def calRockGrade(self, stakes):
        rockGradeList = []
        rockGrade = -1
        for stake in stakes:
            number = 0
            while stake < self.rockEnd[number]:
                number = number + 1
                if number == len(self.rockEnd):
                    break

            if number != len(self.rockEnd):
                if stake < self.rockOrigin[number]:
                    rockGradeList.append(self.rockGrade[number])
                else:
                    rockGradeList.append('大于所有起始范围')
            else:
                rockGradeList.append('小于所有结束范围')

        # print(rockGradeList)
        try:
            # bincount（）：统计非负整数的个数，不能统计浮点数
            counts = np.bincount(rockGradeList)
            # 返回众数
            rockGrade = np.argmax(counts)
        except:
            rockGrade = -2

        return rockGrade


# 选取稳定段数据
def calculateStable(origin, rowDataValue, end):
    rowDataValue = rowDataValue[origin: end + 1]
    mean = np.mean(rowDataValue)

    return mean


# 生成预处理数据文件
def createPreproData(df, address, name):
    # 存放预处理结果的文件夹
    resultDirPath = transAddress(address)
    # 不存在则创建
    if not os.path.exists(resultDirPath):
        os.makedirs(resultDirPath)
    # 预处理文件路径
    resultFilePath = os.path.join(resultDirPath, name)
    # 生成预处理文件
    df.to_csv(resultFilePath)

    return resultFilePath


# 调用该函数处理文件夹下所有txt文件，dirAddress为相对DataPreprocessing.py的路径，index为需要使用数据的列索引，即参数名称
def AllTxtHandle(dirAddress, index):
    # 因为python的相对路径默认为相对运行文件的路径，所以转为绝对路径
    address = transAddress(dirAddress)
    dataDict = {}
    # 便利文件夹下所有文件
    for root, dirs, files in os.walk(address):
        for file in files:
            path = os.path.join(root, file)
            # 处理单个txt文件
            dataDict[file] = oneTxtHandle(path, index)

    return dataDict


# 调用该函数读取单个txt文件数据，oneDataAddress为相对DataPreprocessing.py的路径，index为需要使用数据的列索引，即参数名称
def oneTxtHandle(oneDataAddress, index):
    # 因为python的相对路径默认为相对运行文件的路径，所以转为绝对路径
    address = transAddress(oneDataAddress)
    # 读入数据
    basicData = pd.read_csv(address, sep='\t', index_col=False)
    # 选取需要的列组成DataFrame
    frame = pd.DataFrame(basicData, columns=index)
    # 删除缺失行：当行中有任意一个值为缺失时，删除行
    # print(frame)
    data_del_lack_row = frame.dropna()
    # 处理误差
    # print(data_del_lack_row)
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
    base_dir = os.path.dirname(os.path.abspath('__file__'))
    absolutePath = os.path.normpath(os.path.join(base_dir, relativePath))
    return absolutePath


# 解压缩函数
def AllUnZip():
    zipDirPath = transAddress(zipAddress)
    txtDirPath = transAddress(txtAddress)
    # 不存在txt存放目录则创建
    if not os.path.exists(txtDirPath):
        os.makedirs(txtDirPath)
    # 遍历压缩包目录下所有压缩包
    for root, dirs, files in os.walk(zipDirPath):
        for file in files:
            filePath = os.path.join(root, file)
            # 解压单个压缩包
            r = zipfile.is_zipfile(filePath)
            if r:
                # 如果解压缩文件并不存在，解压缩该压缩包
                if not os.path.exists(txtDirPath + file[0:-4] + '.txt'):
                    fz = zipfile.ZipFile(filePath, 'r')
                    for zipFile in fz.namelist():
                        fz.extract(zipFile, txtDirPath)
                        fz.close()
            else:
                print('This is not zip')

# if '__name__' == '__main__':
# rf = RF()
# rf.RFData()
# adaCost = AdaCost()
# adaCost.adaCostData()
