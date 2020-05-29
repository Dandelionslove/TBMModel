import matplotlib
import pandas as pd
import os
import numpy as np
import zipfile
import matplotlib.pyplot as plt

# 相对路径均为相对DataPreprocessing.py的路径
# 存放txt数据的文件夹
txtAddress = 'txtData'
# 存放预处理数据的文件夹
preDataAddress = 'data2'
# 存放zip压缩包的文件夹
zipAddress = '../../Data'
# 围岩等级表地址
rockFormAddress = 'TBMData/围岩等级信息统计表-现场工程师统计.xlsx'
# 存放可视化图片
picDirAddress = '../../DataPic'


class RF:
    def __init__(self):
        # 存放预处理数据地址
        self.dataPath = 'data1'  # preDataAddress#
        # 预处理数据文件名
        self.DataFileName = 'train.csv'  # 'allIndexRF.csv'#
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
            # self.RFIndex = list(data.keys())
            torque = getEMA(data['刀盘扭矩'].values)
            F = getEMA(data['总推进力'].values)
            result = {}
            stableList = []
            i = 0
            while i < len(torque) - 101:

                origin = i
                while origin < len(torque) - 100:
                    if torque[origin] > 100:
                        break
                    origin = origin + 1
                number = origin
                n = 0
                while number < len(torque):
                    if torque[number] < 100:
                        n = n + 1
                    if n > 50:
                        break
                    number = number + 1
                end = number
                if np.mean(torque[origin:end]) < 100:
                    i = end + 1
                    continue
                plt.plot(torque, color='blue', label='T')
                # plt.plot(F, color='green', label='F')
                # plt.plot(getEMA(data['推进速度'].values), color='red', label='S')
                #
                # # 设置图标标题
                # plt.legend()
                # plt.title(date, fontsize=24)
                # plt.xlim([origin, end])
                #
                # # 设置坐标轴标签
                # plt.xlabel("time/s")
                # plt.ylabel("")
                # # 设置刻度标记的大小
                # plt.tick_params(axis='both', labelsize=14)
                # # 转绝对地址
                # picDirPath = transAddress(picDirAddress)
                # # 不存在则创建
                # if not os.path.exists(picDirPath):
                #     os.makedirs(picDirPath)
                # picName = date[10:-4] + ':' + str(origin) + '~' + str(end) + '.png'
                # # 预处理文件路径
                # picFilePath = os.path.join(picDirPath, picName)
                # # 生成图片
                # plt.savefig(picFilePath)
                # # 清空缓存
                # plt.close()
                #为1取该循环段数据，为0删去
                flag = 1
                riseNum = rise(origin, end, torque, F)
                stableList = stable(riseNum, end, torque)




                if riseNum == 0:
                    flag = 0
                else:
                    result = self.calculateRise(data, riseNum)


                for index in self.RFStableIndex:
                    result['稳定段' + index + '均值'] = calculateStable(stableList[0], getEMA(data[index].values),
                                                                   stableList[1])
                i = end
                i = i + 1


                # 当数据中有任意为0时筛去该循环段数据
                for x in result:
                    if result[x] == 0:
                        flag = 0
                        # print(1)
                        # picName = date[10:-4] + ':' + str(origin) + '~' + str(end) + '.png'
                        # print(picName)
                        # print('上升段' + str(riseNum) + '~' + str(riseNum + 30))
                        # print('稳定段' + str(stableList[0]) + '~' + str(stableList[1]))
                        break

                # 当稳定段刀盘扭矩值小于500时筛去该循环段数据。因为可能存在稳定段平稳略大于0的情况
                if np.mean(torque[stableList[0]:stableList[1]]) < 500:
                    # print(2)
                    # picName = date[10:-4] + ':' + str(origin) + '~' + str(end) + '.png'
                    # print(picName)
                    # print('上升段' + str(riseNum) + '~' + str(riseNum + 30))
                    # print('稳定段' + str(stableList[0]) + '~' + str(stableList[1]))
                    flag = 0

                # # 当稳定段起点与上升段第30s距离超过600s时舍去。
                # if stableList[0] - riseNum - 30 > 600:
                #     flag = 0

                # 当稳定段数据少于50时，筛去该循环段数据，因为可能存在只有两个点的情况
                if stableList[1] - stableList[0] < 50:
                    # print(3)
                    # picName = date[10:-4] + ':' + str(origin) + '~' + str(end) + '.png'
                    # print(picName)
                    # print('上升段' + str(riseNum) + '~' + str(riseNum + 30))
                    # print('稳定段' + str(stableList[0]) + '~' + str(stableList[1]))
                    flag = 0

                # if isRise(torque[riseNum:riseNum + 31]) < 20:
                #     print(4)
                #     picName = date[10:-4] + ':' + str(origin) + '~' + str(end) + '.png'
                #     print(picName)
                #     print('上升段' + str(riseNum) + '~' + str(riseNum + 30))
                #     print('稳定段' + str(stableList[0]) + '~' + str(stableList[1]))
                #     flag = 0

                # # 当前600s还没有选择好上升段起点时，筛去该数据。
                # if riseNum - origin > 600:
                #     flag = 0

                if flag == 1:
                    self.resultList.append(result)
                    # # plot根据列表绘制出有意义的图形
                    # plt.plot(torque, color='blue', label='T')
                    # plt.plot(getEMA(data['总推进力'].values), color='green', label='F')
                    # plt.plot(getEMA(data['推进速度'].values), color='red', label='S')
                    # plt.axvline(x=riseNum, ls="-", lw=1, c="black", label='Rise')  # 添加垂直直线
                    # plt.axvline(x=riseNum + 30, ls="-", lw=1, c="black")
                    # plt.axvline(x=stableList[0], ls="-", lw=1, c="purple", label='Stable')
                    # plt.axvline(x=stableList[1], ls="-", lw=1, c="purple")
                    #
                    # # 设置图标标题
                    # plt.legend()
                    # plt.title(date, fontsize=24)
                    # plt.xlim([origin, end])
                    # # 设置坐标轴标签
                    # plt.xlabel("time/s")
                    # plt.ylabel("")
                    # # 设置刻度标记的大小
                    # plt.tick_params(axis='both', labelsize=14)
                    # # 转绝对地址
                    # picDirPath = transAddress(picDirAddress)
                    # # 不存在则创建
                    # if not os.path.exists(picDirPath):
                    #     os.makedirs(picDirPath)
                    # picName = date[10:-4] + ':' + str(origin) + '~' + str(end) + '.png'
                    # print(picName)
                    # print('上升段' + str(riseNum) + '~' + str(riseNum + 30))
                    # print('稳定段' + str(stableList[0]) + '~' + str(stableList[1]))
                    # # 预处理文件路径
                    # picFilePath = os.path.join(picDirPath, picName)
                    # # 生成图片
                    # plt.savefig(picFilePath)
                    # # 清空缓存
                    # plt.close()

        # print(result)

        # print(self.resultList)
        df = pd.DataFrame(self.resultList)
        # print(df)
        # 生成预处理数文件
        createPreproData(df, self.dataPath, self.DataFileName)

        # return df

    # 判断上升段，并选取上升段数据
    def calculateRise(self, data, number):
        result = {}
        for name in self.RFIndex:
            info = data[name].values
            info = getEMA(info[number + 1:number + 31])
            mean = info.mean()
            var = info.var()
            result[name + '均值'] = mean
            if name in ['总推进力', '刀盘功率', '刀盘扭矩', '推进速度', '刀盘速度给定', '刀盘转速']:
                result[name + '方差'] = var

        return result


class AdaCost:
    def __init__(self):
        # 预处理数据文件名
        self.DataFileName = 'adaCostPreData.csv'  # 'allIndexAdaCost.csv'#'
        # AdaCostIndex为adacost需要使用数据的列索引，即参数名称，额外加入刀盘扭矩判断上升段与稳定段
        self.AdaCostIndex = ['桩号', '刀盘运行时间', '撑靴压力', '刀盘扭矩', '刀盘转速', '撑靴泵压力', '左撑靴俯仰角', '控制泵压力',
                             '右撑靴俯仰角', '左撑靴滚动角', '左撑靴油缸行程检测', '右撑靴滚动角',
                             '右撑靴油缸行程检测']  # , '刀盘转速电位器值设定值'
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
            # self.AdaCostIndex = list(data.keys())
            torque = getEMA(data['刀盘扭矩'].values)
            i = 0
            while i < len(torque) - 101:
                origin = i
                while origin < len(torque) - 100:
                    if torque[origin] > 100:
                        break
                    origin = origin + 1
                number = origin
                n = 0
                while number < len(torque):
                    if torque[number] < 100:
                        n = n + 1
                    if n > 50:
                        break
                    number = number + 1
                end = number
                if np.mean(torque[origin:end]) < 100:
                    i = end + 1
                    continue
                stableList = stable(origin, end, torque)


                result = {}
                for name in self.AdaCostIndex:
                    if name != '桩号' and name != '刀盘扭矩':
                        result[name + '均值'] = calculateStable(stableList[0], getEMA(data[name].values), stableList[1])
                result['围岩等级'] = self.calRockGrade(data['桩号'].values[stableList[0]: stableList[1]])

                i = end
                i = i + 1

                flag = 1

                if result['围岩等级'] < 0:
                    flag = 0

                for x in result:
                    if result[x] == 0:
                        flag = 0
                        break

                if np.mean(torque[stableList[0]:stableList[1]]) < 500:
                    flag = 0

                # if stableList[0] - riseNum - 30 < 0:
                #     flag = 0

                if stableList[1] - stableList[0] < 50:
                    flag = 0

                # if riseNum - origin > 600:
                #     flag = 0

                if flag == 1:
                    self.resultList.append(result)

        # print(self.resultList)
        df = pd.DataFrame(self.resultList)
        # print(df)
        # 生成预处理数据文件
        createPreproData(df, preDataAddress, self.DataFileName)

        # return df

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
            # bincount（）：统计非负整数的个数
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
            if file.endswith('txt'):
                try:
                    dataDict[file] = oneTxtHandle(path, index)
                except:
                    print(file + ' has a problem in oneTxtHandle')
            else:
                print(file + ' is not a txt')

    return dataDict


# 调用该函数读取单个txt文件数据，oneDataAddress为相对DataPreprocessing.py的路径，index为需要使用数据的列索引，即参数名称
def oneTxtHandle(oneDataAddress, index):
    # 因为python的相对路径默认为相对运行文件的路径，所以转为绝对路径
    address = transAddress(oneDataAddress)
    # 读入数据
    basicData = pd.read_csv(address, sep='\t', index_col=False)
    # 选取需要的列组成DataFrame
    # basicData = basicData.dropna(axis=1, how='all')
    # index = list(basicData.keys())[2:]
    frame = pd.DataFrame(basicData, columns=index)
    # frame = pd.DataFrame(basicData, columns=index)
    # 删除缺失行：当行中有任意一个值为缺失时，删除行
    # print(frame)
    data_del_lack_row = frame.dropna()
    # 处理误差
    # print(data_del_lack_row)
    oneTxtData = errorHandle(data_del_lack_row, index)  # data_del_lack_row#
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
                    try:
                        for zipFile in fz.namelist():
                            fz.extract(zipFile, txtDirPath)
                            fz.close()
                    except:
                        print(file + ' has a problem in AllUnZip')
            else:
                print(file + ' is not zip')


def getEMA(data):
    # 平滑值 = a(新数据) + (1-a )(原平滑值)
    a = 0.2
    emas = data.copy()  # 创造一个和cps一样大小的集合
    for i in range(len(data)):
        if i == 0:
            emas[i] = data[i]
        if i > 0:
            emas[i] = (1 - a) * emas[i - 1] + a * data[i]
    return emas


def isRise(data):
    riseNumber = 0
    reduction = 0
    flag = 0
    for i in range(len(data) - 1):
        if data[i + 1] - data[i] > 0:
            riseNumber = riseNumber + 1
        if data[i + 1] - data[i] < -20:
            reduction = reduction + 1

    if reduction > 5:
        riseNumber = 0

    return riseNumber


def slope(data):
    total = 0
    for i in range(len(data) - 1):
        total = (data[i + 1] - data[i]) * (data[i + 1] - data[i]) + total

    return total / 100

def riseEnd(F):
    total = 0
    for i in range(len(F)):
        if F[i] - F[1] > 1000:
            total += 1

    return total

def isDown(F):
    total = 0
    for i in range(len(F) - 1):
        if F[i + 1] - F[i] <= 40:
            total += 1

    return total



def rise(origin, end, torque, F):
    number = origin
    flag = 1
    # 判断是否为上升段，并选取前30个数据
    # while slope(torque[number - 30:number]) < 100 and number > origin + 31:
    #     number = number - 1
    # while slope(torque[number - 30:number]) > 30 and number > origin + 31:
    #     number = number - 1
    # if isRise(torque[number:number + 30]) > 15:
    #     number = 0
    # while riseEnd(F[number - 30:number]) < 5:
    #     if number <= origin:
    #         number = 0
    #         flag = 0
    #         break
    #     number = number - 1
    # if flag != 0:
    #     number = number - 30
    #     # print(number)
    #     while number > origin + 50:
    #         if isDown(F[number - 10:number]) > 8:
    #             break
    #         number = number - 1
    while number < end - 100:
       # if torque[number + 1] - torque[number] > 10 and isRise(torque[number:number + 100]) > 70 and \
       #      isRise(torque[number + 1:number + 31]) > 20 and slope(torque[number:number + 100]) > 90 and \
        if F[number + 1] - F[number] > 50:
            break
        else:
            number = number + 1
    return number


def stable(begin, length, torque):
    number = begin
    if number + 100 < length:
        while (slope(torque[number:number + 100]) > 150 and np.mean(torque[number:number + 100]) > 2000)\
                or (slope(torque[number:number + 100]) > 40 and np.mean(torque[number:number + 100]) <= 2000):
            number = number + 1

    end = number
    # 通过刀盘扭矩时， 判断稳定段终点， 并选取稳定段数据
    while end < length:
        if slope(torque[end:end + 50]) > 100:
            if end - number < 50:
                while (slope(torque[number:number + 100]) > 150 and np.mean(torque[number:number + 100]) > 2000) \
                        or (slope(torque[number:number + 100]) > 40 and np.mean(torque[number:number + 100]) <= 2000):
                    number = number + 1
                    end = number
                end = end + 1
                continue
            break
        elif end + 1 == len(torque):
            break
        else:
            end = end + 1
    stable = []
    stable.append(number)
    stable.append(end + 1)
    return stable
# if '__name__' == '__main__':
# rf = RF()
# rf.RFData()
# adaCost = AdaCost
# adaCost.adaCostData()
