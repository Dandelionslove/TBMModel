##依赖与python版本 
python 3.7.7  
pandas 1.0.3  
numpy 1.16.2  
xlrd 1.2.0
matplotlib 3.1.3

##数据预处理脚本使用方法：
###RF数据预处理使用方法
1.使用之前在TBMModel文件夹同一目录建立名为Data的文件夹，(服务器上为ZhangShuangli/TBMModel/Data)，将zip压缩包放入该Data文件夹中。  
2.安装pandas、numpy、matplotlib和xlrd。(服务器上已经安好）
3.运行/TBMModel/DataPreprocessing/RFPredata.py 文件  
4.预处理csv文件为/TBMModel/TBMDrivingParameters/RF_CART/data/train.csv 
5.txt数据目录为/TBMModel/TBMData/txtData
6.需要数据可视化的话，取消DataPreprocessing.py的193～225行的注释，运行后，可视化图片出现在TBMModel文件夹同一目录的DataPic文件夹中

###adaCost数据预处理使用方法
1.使用之前在TBMModel文件夹同一目录建立名为Data的文件夹，(服务器上为ZhangShuangli/TBMModel/Data)，将zip压缩包放入该Data文件夹中。 
2.将围岩等级信息统计表-现场工程师统计.xlsx放入ZhangShuangli/TBMModel/TBMModel/TBMData文件夹中(服务器上已有)。   
3.安装pandas、numpy、matplotlib和xlrd.  
4.运行/TBMModel/DataPreprocessing/AdaCostPreData.py 文件  
5.预处理csv文件为/TBMModel/TBMData/TBMPreproData/adaCostPreData.csv
6.txt数据目录为/TBMModel/TBMData/txtData
7.需要数据可视化的话，取消DataPreprocessing.py的386～414-行的注释，运行后，可视化图片出现在TBMModel文件夹同一目录的DataPic文件夹中

#####如果需要一次运行出RF和adaCost的预处理数据，在将zip压缩包和信息表放置好并且安装好依赖包之后，直接运行 /TBMModel/DataPreprocessing/AllPreData.py即可，结果如上述。