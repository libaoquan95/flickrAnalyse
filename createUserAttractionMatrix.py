#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pandas import Series, DataFrame


# 构建照片-用户关联矩阵
# param  geoFile：geo数据集
#        phontUserFile：写入照片-用户关联矩阵的文件
# return none
def createPhotoUserMatrix(dataSets, phontUserFile):
    dataSets[['USER_NAME','PHOTO_TIME']].to_csv(phontUserFile, \
            encoding='utf-8', index=True)
    
    
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
        oneFrame = pd.read_csv(culstersFolder + provinces_py[i] + '.csv', \
                               index_col=0)
        oneFrame['province'] = provinces_py[i]
        data.append(oneFrame)
    
    # 合并
    phontAttractionFrame = pd.concat(data)
    # 写入照片-用户景点矩阵文件
    phontAttractionFrame[['clusterId','province']].to_csv(phontAttractionFile,\
                        encoding='utf-8', index=True)
    
    
# 构建用户-景点矩阵
# param:照片-景点关联文件, 照片-用户关联文件
# return none
def createUserAttractionMatrix(phontAttractionFile, phontUserFile, userAttractionFile):
    phontAttractionFrame = pd.read_csv(phontAttractionFile, index_col=0)
    phontUserFrame = pd.read_csv(phontUserFile, index_col=0)
    #print(phontAttractionFrame)
    #print(phontUserFrame)
    
    # 找出所有的用户
    usersFrame = phontUserFrame.drop_duplicates('USER_NAME')
    users = np.array(usersFrame['USER_NAME'])
    
    # 构建用户-景点矩阵
    # 遍历用户信息
    userAttractionData = []
    for userId in users:
        # 找到与此用户关联的照片id
        photoIds = np.array(phontUserFrame[phontUserFrame['USER_NAME'] == userId].index.drop_duplicates())
        # 找到照片ID相关联的景点信息
        attractions = phontAttractionFrame.loc[photoIds, ['clusterId', 'province']]
        # 筛除噪音数据(clusterId == -1)
        attractions = attractions[attractions['clusterId'] != -1]
        
        if(len(attractions) != 0):
            # 获取景点id(省标识_聚类id)
            #attractionIds = attractions.drop_duplicates()
            for (clusterId, province), group in attractions.groupby([attractions['clusterId'],attractions['province']]):
                attractionId = ('%s_%s' % (province, int(clusterId)))
                userAttractionData.append([userId, attractionId, len(group)])
    # 将用户-景点-照片数量关系写入DataFrame
    userAttractionData = np.array(userAttractionData)
    data = {'USER_NAME': userAttractionData[:, 0],    \
            'attractionId': userAttractionData[:, 1], \
            'photoCount': userAttractionData[:, 2]}
    userAttraction = DataFrame(data, columns=['USER_NAME', 'attractionId', 'photoCount'])
    # 写入照片-用户景点矩阵文件
    userAttraction.to_csv(userAttractionFile, encoding='utf-8', index=False)
    

def main():
    baseDir = 'yfcc100m_dataset/'
    
    # 读取数据集
    dataSets = pd.read_csv(baseDir + 'info_0_3.csv', index_col=0)
    
    phontUserFile = baseDir + 'photo-user.csv'
    createPhotoUserMatrix(dataSets, phontUserFile)
    
    culstersFolder = baseDir + 'culsters/'
    phontAttractionFile = baseDir + 'photo-attraction.csv'
    createPhotoAttractionMatrix(culstersFolder, phontAttractionFile)
    
    userAttractionFile = baseDir + 'user-attraction.csv' 
    createUserAttractionMatrix(phontAttractionFile, phontUserFile, userAttractionFile)
main()