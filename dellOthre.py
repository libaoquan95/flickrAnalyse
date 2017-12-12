import numpy as np
import pandas as pd
from pandas import Series, DataFrame

# 数据集预处理
def pretreatment_L(geoFile, addressFile):
    # 从flick-geo-abortchina-china文件中获取照片id,用户id,拍摄时间,经纬度信息
    geoFile = open(geoFile, encoding='utf-8')
    geoDatas = []
    for line in geoFile:
        meteData = line.strip().split('\t')
        geoDatas.append([meteData[0], meteData[1], meteData[3], \
                         meteData[10], meteData[11]])
    geoFile.close()
    geoDatas = np.array(geoDatas)
    data = {'USER_NAME':geoDatas[:, 1], 'PHOTO_TIME':geoDatas[:, 2], \
            'Longitude': geoDatas[:, 3], 'Latitude': geoDatas[:, 4], \
            'PROVINCE':geoDatas[:, 0], 'LOCATION':geoDatas[:, 0]}
    geoFrame = DataFrame(data, columns=['USER_NAME', 'PHOTO_TIME', 'Longitude', 'Latitude', \
                                        'PROVINCE', 'LOCATION'], index = geoDatas[:, 0])
    
    addressFile = open(addressFile, encoding='utf-8')
    for line in addressFile:
        meteData = line.strip().split('\t')
        temp = meteData[2].split(', ')
        temp.reverse()
        geoFrame.loc[meteData[0]]['LOCATION'] = ' '.join(temp)
        geoFrame.loc[meteData[0]]['PROVINCE'] = meteData[1]
    addressFile.close()
    
    return geoFrame

def pretreatment_M(csvFile):
    csvFrame = pd.read_csv(csvFile, index_col=0)
    provinces = ['河北省', '山西省', '内蒙古自治区', '黑龙江省', '吉林省', '辽宁省', '陕西省', \
                 '甘肃省', '青海省', '新疆维吾尔自治区', '宁夏回族自治区', '山东省', '河南省', \
                 '江苏省', '浙江省', '安徽省', '江西省', '福建省', '臺灣', '湖北省', '湖南省',\
                 '广东省', '广西壮族自治区', '海南省', '四川省', '云南省', '贵州省', '西藏自治区', \
                 '北京市', '上海市', '天津市', '重庆市', '澳門', 'HK']
    pro = []
    for i in csvFrame.index:
        flag = 0
        for j in range(len(provinces)):
            # 找到此条地址匹配的省份信息
            if(csvFrame.loc[i].values[-1].find(provinces[j]) != -1):
                pro.append(provinces[j])
                flag = 1
        if(flag == 0):
            pro.append('None')
        print(len(pro))
    csvFrame['provinces'] = pro
    print(csvFrame)
    return 1

def main():
    baseDir = 'yfcc100m_dataset/'
    
    geoFile = baseDir + 'flick-geo-abortchina-china'
    addressFile = baseDir + 'flick-geo-abortchina-china-address'
    geoFrame = pretreatment_L(geoFile, addressFile)
    
    #pretreatment_M(baseDir+'info2.csv')
    
    geoFrame.to_csv('yfcc100m_dataset/info_0_3.csv', encoding='utf-8', index=True)
    
main()