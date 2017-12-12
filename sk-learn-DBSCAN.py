#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import DBSCAN
#import dbscanBaseGeo as myDBSCAN
from pandas import Series, DataFrame
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from geopy.distance import vincenty
from geopy.distance import great_circle

    
# 聚类
# param 待聚类数据
# return 聚类结果,聚类统计
def my_dbscan(dataSets, provinceName, my_eps=0.001, my_min_samples=8):
    #y_pred = DBSCAN(eps = 0.5, min_samples = 10).fit_predict(proGeo)
    #DBSCANs = myDBSCAN.DBSCAN(eps=1, minPts=1)
    #y_pred, count = DBSCANs.fit_predict(proGeo)
    
    # 获取某一省份的照片id集
    dataIds = dataSets[dataSets['PROVINCE'] == provinceName].index
    # 根据照片id集获取经纬度
    culsterData = dataSets.loc[dataIds, ['Longitude', 'Latitude']]
    
    y_pred = DBSCAN(eps = my_eps, min_samples = my_min_samples).fit_predict(culsterData)
    culsterData['clusterId'] = y_pred
    
    # 统计聚类结果
    culsterResult = {}
    culsterResult['DataCount'] = len(culsterData) # 聚类数据的数据量
    culsterResult['CulsterAndCount'] = {}         # 每一个聚类及数量
    
    for i in range(culsterResult['DataCount']):
        culsterResult['CulsterAndCount'].setdefault(y_pred[i], 0)
        culsterResult['CulsterAndCount'][y_pred[i]] += 1
    
    culsterResult['NoisyCount'] = culsterResult['CulsterAndCount'][-1]        # 噪音点数量
    culsterResult['CulsterCount'] = len(culsterResult['CulsterAndCount']) - 1 # 聚类数量
    
    
    #print('总数据 %d 条, 有效聚类 %d 条, 噪音点 %d 条, 有 %d 个类' \
    #      % (culsterResult['DataCount'], culsterResult['DataCount'] - culsterResult['NoisyCount'],\
    #        culsterResult['NoisyCount'], culsterResult['CulsterCount']))

    # 剔除噪音点, 即clusterId=-1的点
    #print(culsterData[culsterData.clusterId != -1])
    #print(culsterData)
    return culsterData, culsterResult
    
# 画散点图
# param Data:数据, w:图片宽度, h:图片高度, solit:散点大小, picTltle:图片名
# return plt,fig
def drawScatter(Data, culsterResult, w=5, h=5, solit=10, picTltle='title'):
    plt.figure()             
    fig = plt.gcf()
    fig.set_size_inches(w,  h)
    
    plt.scatter(Data['Longitude'], Data['Latitude'], c=Data['clusterId'], s=solit)
    plt.title('%s\nSum %d, Culster %d, Noisy %d, have %d culsters' \
          % (picTltle, culsterResult['DataCount'], \
             culsterResult['DataCount'] - culsterResult['NoisyCount'],\
             culsterResult['NoisyCount'], culsterResult['CulsterCount']))
    
    plt.show()
    plt.close(0)
    return plt, fig

# 画条形图
# param Data:数据, w:图片宽度, h:图片高度, solit:散点大小, picTltle:图片名
# return plt,fig
def drawBar(Data, culsterResult, w=5, h=5, solit=10, picTltle='title'):
    y = []
    index =  np.arange(culsterResult['CulsterCount'])
    
    maxCount = 0#culsterResult['CulsterAndCount'][0]
    minCount = sys.maxsize#culsterResult['CulsterAndCount'][0]
    for i in range(culsterResult['CulsterCount']):
        y.append(culsterResult['CulsterAndCount'][i])
        maxCount = max(maxCount, culsterResult['CulsterAndCount'][i])
        minCount = min(minCount, culsterResult['CulsterAndCount'][i])
        
    plt.figure()        
    fig = plt.gcf() 
    fig.set_size_inches(w,  h)
    
    plt.bar(left=0,bottom=index , width=y, color='#4093c6',height=0.5, orientation='horizontal')
    
    plt.title('%s\n %d culsters, max is %d, min is %d' \
          % (picTltle, culsterResult['CulsterCount'], maxCount, minCount))
    
    plt.show()
    plt.close(0)
    
    return plt,fig

# 用距离最远的两点为直径，做圆
def calArea(Data, culsterResult, fileName='none'):
    outFile = open(fileName+"_distance.txt", 'w', encoding='UTF-8')
    outFile.write('聚类id\t最大距离m\n')
    for k in range(culsterResult['CulsterCount']):
        maxdistance = 0
        a = Data[Data['clusterId'] == k]
        for i in a.index:
            for j in a.index:
                pointA = (a.loc[i].values[1], a.loc[i].values[0])
                pointB = (a.loc[j].values[1], a.loc[j].values[0])
                maxdistance = max(maxdistance, vincenty(pointA, pointB).meters)
        outFile.write(('%d\t%f\n') % (k, maxdistance))
        print(('%d,%fm') % (k, maxdistance))
    outFile.close()


def main():
    baseDir = 'yfcc100m_dataset/'
    
    # 读取数据集
    dataSets = pd.read_csv(baseDir + 'info_0_3.csv', index_col=0)
    
    provinces = ['辽宁省', '陕西省', '浙江省', '重庆市', '黑龙江省',         \
                 '安徽省', '山西省', '山东省', '上海市', '新疆维吾尔自治区', \
                 '湖南省', '甘肃省', '河南省', '北京市', '内蒙古自治区',     \
                 '云南省', '江西省', '湖北省', '吉林省', '宁夏回族自治区',   \
                 '天津市', '福建省', '四川省', '臺灣',   '广西壮族自治区',   \
                 '广东省', '河北省', '海南省', '澳門',   '西藏自治区',       \
                 '贵州省', '江苏省', '青海省', 'HK']
    
    provinces_py = ['LN',  'ShanX', 'ZJ',  'CQ',    'HLJ', \
                    'AH',  'SanX',  'SD',  'SH',    'XJ',  \
                    'HuN', 'GS',    'HeN', 'BJ',    'NMG', \
                    'YN',  'JX',    'HuB', 'JL',    'NX',  \
                    'TJ',  'FJ',    'SC',  'TW',    'GX',  \
                    'GD',  'HeB',   'HaiN','Macro', 'XZ',  \
                    'GZ',  'JS',    'QH',  'HK']
    
    #for provincesIndex in range(len(provinces)):
    provincesIndex = 6
    culsters, culsterResult = my_dbscan(dataSets, provinces[provincesIndex], 0.0001, 15)
    
    print('总数据 %d 条, 有效聚类 %d 条, 噪音点 %d 条, 有 %d 个类' \
          % (culsterResult['DataCount'], culsterResult['DataCount'] - culsterResult['NoisyCount'],\
            culsterResult['NoisyCount'], culsterResult['CulsterCount']))
    
    # 无噪音点散点图
    pltS, figS = drawScatter(culsters[culsters.clusterId != -1], culsterResult, 5, 5, 10, provinces_py[provincesIndex])
    # 有噪音点散点图
    pltSN, figSN = drawScatter(culsters, culsterResult, 5, 5, 10, provinces_py[provincesIndex])
    # 聚类和聚类数量条形图,无噪音点
    pltB, figB = drawBar(culsters, culsterResult, 5, 5, 10, provinces_py[provincesIndex])
    
    # 计算每个聚类的实际面积
    #calArea(culsters, culsterResult, baseDir + 'culsters/' + provinces_py[provincesIndex])
    
    # 将聚类结果写入到文件中
    culsters.to_csv(baseDir + 'culsters/' + provinces_py[provincesIndex] + '.csv', encoding='utf-8', index=True)
    
    # 将聚类结果写入到图片中
    figS.savefig(baseDir + 'culsters/' + provinces_py[provincesIndex] + '_scatter.png',  dpi=100)
    figSN.savefig(baseDir + 'culsters/' + provinces_py[provincesIndex] + '_scatter_noisy.png',  dpi=100)
    figB.savefig(baseDir + 'culsters/' + provinces_py[provincesIndex] + '_bar.png',  dpi=100)
    
    
main()
