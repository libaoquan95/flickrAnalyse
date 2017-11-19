#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import DBSCAN
#import dbscanBaseGeo as myDBSCAN
from pandas import Series, DataFrame
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

'''
def test_dbscan():
    X1, y1=datasets.make_circles(n_samples=5000, factor=.6,noise=.05)
    X2, y2 = datasets.make_blobs(n_samples=1000, n_features=2, \
                                 centers=[[1.2,1.2]], cluster_std=[[.1]],\
                                 random_state=9)
    
    X = np.concatenate((X1, X2))
    plt.scatter(X[:, 0], X[:, 1], marker='o')
    plt.show()
    
    print(X1)
    
    y_pred = DBSCAN(eps = 0.1, min_samples = 10).fit_predict(X)
    #y_pred = myDBSCAN.DBSCAN(eps = 0.1, minPts = 10).fit_predict(X)
    
    plt.scatter(X[:, 0], X[:, 1], c=y_pred)
    plt.show()
    
    print(X)
 '''   
    
    
# 按省份信息筛选数据，联立省份和Geo信息
# param geoFile:geo信息文件, addressFile:地址信息文件, province:省份名称 
# return 某一省份的Geo信息，以id为索引，只包含经纬度值
def selectData(geoFile, addressFile, province):
    #读取数据集，获取经纬度信息
    inFile = open(geoFile, encoding='utf-8')
    datas = []
    for line in inFile:
        meteData = line.strip().split('\t')
        datas.append([meteData[0], meteData[10], meteData[11]])
    inFile.close()
    
    # 将经纬度数据存入DataFrame类型geoFrame
    geoDatas = np.array(datas)
    data = {'lon': geoDatas[:, 1], 'lat': geoDatas[:, 2]}
    geoFrame = DataFrame(data, columns=['lon', 'lat'],index = geoDatas[:, 0])
    #print(geoFrame)
    
    #读取数据集，获取地址信息
    inFile = open(addressFile, encoding='utf-8')
    datas = []
    for line in inFile:
        meteData = line.strip().split('\t')
        datas.append(meteData)
    inFile.close()
    
    # 将地址数据存入DataFrame类型addressFrame
    addressDatas = np.array(datas)
    data = {'province': addressDatas[:, 1], 'address': addressDatas[:, 2]}
    addressFrame = DataFrame(data, columns=['province', 'address'],index = addressDatas[:, 0])
    #print(addressFrame)
    
    # 获取某一省份的照片id集
    dataIds = addressFrame[addressFrame['province'] == province].index
    #print(geoFrame['lon','lat'].loc[dataIds])
    
    # 根据照片id集获取经纬度
    proGeo = geoFrame.loc[dataIds, ['lon', 'lat']]
    #print(proGeo)
    return proGeo
    
    
# 聚类
# param 待聚类数据
# return 聚类结果,聚类统计
def my_dbscan(culsterData, my_eps=0.001, my_min_samples=8):
    #y_pred = DBSCAN(eps = 0.5, min_samples = 10).fit_predict(proGeo)
    #DBSCANs = myDBSCAN.DBSCAN(eps=1, minPts=1)
    #y_pred, count = DBSCANs.fit_predict(proGeo)
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
    return culsterData[culsterData.clusterId != -1],culsterResult
    
# 画图
# param Data:数据, w:图片宽度, h:图片高度, solit:散点大小, picTltle:图片名
# return plt,fig
def drawScatter(Data, w=5, h=5, solit=10, picTltle='title'):             
    fig = plt.gcf()
    fig.set_size_inches(w,  h)
    
    plt.scatter(Data['lon'], Data['lat'], c=Data['clusterId'], s=solit)
    plt.title(picTltle)
    return plt, fig

def main():
    baseDir = 'yfcc100m_dataset-0/'
    geoFile = baseDir + 'flick-0-geo-abortchina-china'
    addressFile = baseDir + 'flick-0-geo-abortchina-china-address'
    
    provinces = ['辽宁省', '陕西省', '浙江省', '重庆市', '黑龙江省',         \
                 '安徽省', '山西省', '山东省', '上海市', '新疆维吾尔自治区', \
                 '湖南省', '甘肃省', '河南省', '北京市', '内蒙古自治区',     \
                 '云南省', '江西省', '湖北省', '吉林省', '宁夏回族自治区',   \
                 '天津市', '福建省', '四川省', '臺灣',   '广西壮族自治区',   \
                 '广东省', '河北省', '海南省', '澳門',   '西藏自治区',       \
                 '贵州省', '江苏省', '青海省', 'HK']
    
    provinces_py = ['Liao Ning', 'Shan Xi', 'Zhe Jiang', 'Chong Qing', 'Hei Long Jiang',         \
                    'An Hui',    'San Xi',  'San Dong',  'Shang Hai',  'Xing Jiang', \
                    'Hu Nan',    'Gan Su',  'He Nan',    'Bei Jing',   'Nei Mong Gu',     \
                    'Yun Nam',   'Jiang Xi','Hu Bei',    'Jin Lin',    'Ning Xia',   \
                    'Tian Jin',  'Fu Jian', 'Si Chuan',  'Tai Wan',    'Guang Xi',   \
                    'Guang Dong','He Bei',  'Hai Nan',   'Macro',      'Xi Zhang',       \
                    'Gui Zhou',  'Jiang Su','Qin Hai',   'Hong Kong']
    
    provincesIndex = 23
    proGeo = selectData(geoFile, addressFile, province=provinces[provincesIndex])
    
    culsters, culsterResult = my_dbscan(proGeo, 0.01, 8)
    
    print('总数据 %d 条, 有效聚类 %d 条, 噪音点 %d 条, 有 %d 个类' \
          % (culsterResult['DataCount'], culsterResult['DataCount'] - culsterResult['NoisyCount'],\
            culsterResult['NoisyCount'], culsterResult['CulsterCount']))
    
    plt, fig = drawScatter(culsters, 5, 5, 10, provinces_py[provincesIndex])
    plt.show()
    
    #fig.savefig('yfcc100m_dataset-0/' + province + '.png',  dpi=100)
    #test_dbscan()
    
main()