##依赖与python版本 
python 3.7.7  
pandas 1.0.3  
numpy 1.16.2

##RF数据预处理使用方法
1.使用之前在TBMModel文件夹下建立名为TBMData的文件夹，将解压后的txt数据文件放入TBMData文件夹中。  
2.导入DataPreprocess文件和各个依赖。  
3.实例化RF类  
4.调用RF类中的RFData函数（无参数）  
5.输出结果实例：  
<font size=1>*[{'总推进力均值': 0.0, '总推进力方差': 0.0, '刀盘功率均值': 149.0, '刀盘功率方差': 0.0, '刀盘扭矩均值': 2.5478929999594886, '刀盘扭矩方差': 2.5967581544120426, '推进速度均值': 136.59146118164062, '推进速度方差': 0.0, '刀盘速度给定均值': 87.26666666666667, '刀盘速度给定方差': 4002.4288888888896, '刀盘转速均值': 3352.0327164967853, '刀盘转速方差': 4497586.123340651, '稳定段刀盘转速均值': 7307.536246163504, '稳定段推进速度均值': 136.59146118164062},   
{'总推进力均值': 0.0, '总推进力方差': 0.0, '刀盘功率均值': 149.0, '刀盘功率方差': 0.0, '刀盘扭矩均值': 2.5478929999594886, '刀盘扭矩方差': 2.5967581544120426, '推进速度均值': 136.59146118164062, '推进速度方差': 0.0, '刀盘速度给定均值': 87.26666666666667, '刀盘速度给定方差': 4002.4288888888896, '刀盘转速均值': 3352.0327164967853, '刀盘转速方差': 4497586.123340651, '稳定段刀盘转速均值': 7307.536246163504, '稳定段推进速度均值': 136.59146118164062}]*</font>

##核心代码
RF类：

	class RF:
	    def __init__(self):
	        # Address为存放txt文件夹相对于DataPreprocessing.py的路径
	        self.Address = '../TBMData'
	        # RFIndex为RF需要使用数据的列索引，即参数名称
	        self.RFIndex = ['总推进力', '刀盘功率', '刀盘扭矩', '推进速度', '刀盘速度给定', '刀盘转速']
	        self.result = {}
	        self.resultList = []
	        #处理原始数据的缺失和误差
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
	
	                    #将单个循环段数据放入数据列表中
	                    self.resultList.append(self.result)
	
	                    number = number + 31
	
	                else:
	                    number = number + 1
	        # print(self.resultList)
	        return self.resultList