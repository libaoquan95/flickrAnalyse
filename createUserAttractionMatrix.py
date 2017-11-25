#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pandas import Series, DataFrame


# 构建照片-用户关联矩阵
# param  geoFile：geo数据集
#        phontUserFile：写入照片-用户关联矩阵的文件
# return none
def createPhotoUserMatrix(geoFile, phontUserFile):
    #读取数据集，获取经纬度信息
    inFile = open(geoFile, encoding='utf-8')
    datas = []
    for line in inFile:
        meteData = line.strip().split('\t')
        datas.append([meteData[0], meteData[1], meteData[3]])
    inFile.close()
    
    # 将照片-用户关联数据存入DataFrame类型photoUserFrame
    photoUserData = np.array(datas)
    data = {'userId': photoUserData[:, 1], 'takenDate': photoUserData[:, 2]}
    photoUserFrame = DataFrame(data, columns=['userId', 'takenDate'],index = photoUserData[:, 0])
    #print(photoUserFrame)
    photoUserFrame.to_csv(phontUserFile, encoding='utf-8', index=True)
    
    
# 构建照片-景点关联矩阵，即合并所有省份的分类信息
# param  culstersFolder：照片聚类后的文件夹，
#        phontUserFile：写入照片-用户景点矩阵的文件
# return none
def createPhotoAttractionMatrix(culstersFolder, phontAttractionFile):
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
    
    data = []
    for i in range(len(provinces)):
        oneFrame = pd.read_csv(culstersFolder + provinces_py[i] + '.csv', index_col=0)
        oneFrame['province'] = provinces_py[i]
        data.append(oneFrame)
    
    # 合并
    phontAttractionFrame = pd.concat(data)
    # 写入照片-用户景点矩阵文件
    phontAttractionFrame.to_csv(phontAttractionFile, encoding='utf-8', index=True)
    
    
# 构建用户-景点矩阵
# param:照片-景点关联文件, 照片-用户关联文件
# return none
def createUserAttractionMatrix(phontAttractionFile, phontUserFile, userAttractionFile):
    phontAttractionFrame = pd.read_csv(phontAttractionFile, index_col=0)
    phontUserFrame = pd.read_csv(phontUserFile, index_col=0)
    #print(phontAttractionFrame)
    #print(phontUserFrame)
    
    # 找出所有的用户
    usersFrame = phontUserFrame.drop_duplicates('userId')
    #print(usersFrame)
    users = np.array(usersFrame['userId'])
    #print(users)
    
    # 构建用户-景点矩阵
    # 遍历用户信息
    userAttractionData = []
    for userId in users:
        # 找到与此用户关联的照片id
        photoIds = np.array(phontUserFrame[phontUserFrame['userId'] == userId].index.drop_duplicates())
        #print(userId)
        #print(photoIds)
        
        # 找到照片ID相关联的景点信息
        attractions = phontAttractionFrame.loc[photoIds, ['clusterId', 'province']]
        attractions = attractions.dropna(subset=['province']) # 删除噪音数据
        #attractionIds = attractions.drop_duplicates()
        #print(attractionIds)
        for (clusterId, province), group in attractions.groupby([attractions['clusterId'],\
                                            attractions['province']]):
            if(int(clusterId) != -1):
                attractionId = ('%s_%s' % (province, int(clusterId)))
                userAttractionData.append([userId, attractionId, len(group)])
    
    # 将用户-景点-照片数量关系写入DataFrame
    userAttractionData = np.array(userAttractionData)
    data = {'userId': userAttractionData[:, 0], 'attractionId': userAttractionData[:, 1], \
            'photoCount': userAttractionData[:, 2]}
    userAttraction = DataFrame(data, columns=['userId', 'attractionId', 'photoCount'])
    #print(userAttraction)
    # 写入照片-用户景点矩阵文件
    userAttraction.to_csv(userAttractionFile, encoding='utf-8', index=False)
    

def main():
    baseDir = 'yfcc100m_dataset/'
    
    geoFile = baseDir + 'flick-geo-abortchina-china'
    phontUserFile = baseDir + 'photo-user.csv'
    #createPhotoUserMatrix(geoFile, phontUserFile)
    
    culstersFolder = baseDir + 'culsters/'
    phontAttractionFile = baseDir + 'photo-attraction.csv'
    #createPhotoAttractionMatrix(culstersFolder, phontAttractionFile)
    
    userAttractionFile = baseDir + 'user-attraction.csv' 
    #createUserAttractionMatrix(phontAttractionFile, phontUserFile, userAttractionFile)
main()