import numpy as np
import pandas as pd
from pandas import Series, DataFrame

# 把保存聚类结果的csv转成json
# province = -1时转换全部省份
# clusterId = -2时转换某省份全部聚类结果（不显示噪音点）
def toJson(provinceId, clusterId):
    
    dataFile = open('mapMark/data.js', 'w')
    nameFile = open('mapMark/name.js', 'w')
    
    dataFile.write('var data = {"data":[\n')
    pointCount = 0
    culsterCount = 0
    
    '''
    provinces = ['辽宁省', '陕西省', '浙江省', '重庆市', '黑龙江省',         \
             '安徽省', '山西省', '山东省', '上海市', '新疆维吾尔自治区', \
             '湖南省', '甘肃省', '河南省', '北京市', '内蒙古自治区',     \
             '云南省', '江西省', '湖北省', '吉林省', '宁夏回族自治区',   \
             '天津市', '福建省', '四川省', '臺灣',   '广西壮族自治区',   \
             '广东省', '河北省', '海南省', '澳門',   '西藏自治区',       \
             '贵州省', '江苏省', '青海省', 'HK']
    '''
    
    provinces_py = ['LN',  'ShanX', 'ZJ',  'CQ',    'HLJ', \
                    'AH',  'SanX',  'SD',  'SH',    'XJ',  \
                    'HuN', 'GS',    'HeN', 'BJ',    'NMG', \
                    'YN',  'JX',    'HuB', 'JL',    'NX',  \
                    'TJ',  'FJ',    'SC',  'TW',    'GX',  \
                    'GD',  'HeB',   'HaiN','Macro', 'XZ',  \
                    'GZ',  'JS',    'QH',  'HK']
    
    # 根据输入获取待转换的省份列表
    provinceArray = []
    if provinceId == -1:
        provinceArray = provinces_py
    else:
        provinceArray.append(provinces_py[provinceId])
        
    for j in range(len(provinceArray)):
        province = provinceArray[j]
        dataSet = pd.read_csv('yfcc100m_dataset/culsters/' + province +'.csv', index_col=0)
        
        # 根据输入获取待转换的聚类id列表
        clusterIdArray = []
        if clusterId == -2:
            clusterIdArray = np.array(dataSet['clusterId'].drop_duplicates())
        else:
            clusterIdArray.append(clusterId)
            
        for i in range(len(clusterIdArray)):
            # 不转换噪音点
            if clusterIdArray[i] != -1:
                dataSet_i = dataSet[dataSet['clusterId'] == clusterIdArray[i]]

                # 写入聚类点
                for indexs in dataSet_i.index:
                    dataFile.write(('\t[%f,%f,%d],\n') % \
                                  (dataSet_i.loc[indexs].values[0],\
                                   dataSet_i.loc[indexs].values[1],\
                                   culsterCount));
                    pointCount = pointCount + 1
                culsterCount += 1
                    
    dataFile.write(('],\n"pointCount":%d,\n"culsterCount":%d}\n') \
        % (pointCount, culsterCount))
    dataFile.close()
    nameFile.close()


def main():
    '''
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
    '''
    
    provinceId = 13
    clusterId = -2
    toJson(provinceId, clusterId)

main()
