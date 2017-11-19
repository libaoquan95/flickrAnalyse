import numpy as np
import matplotlib.pyplot as plt
import math
import time
from geopy.distance import vincenty
from geopy.geocoders import Nominatim

UNCLASSIFIED = False
NOISE = 0

# 读取数据集，获得照片的元数据集合
# param  数据集路径,数据集分隔符
# return 照片的元数据集合，字典形式
# 数据集格式
# [0]	Photo/video identifier	照片/视频标识符
# [1]	User NSID	用户NSID
# [2]	Date taken	拍摄日期
# [3]	Longitude	经度
# [4]	Latitude	纬度
# [5]	Photo/video page URL	照片/视频页面URL
# [6]	Photos/video marker (0 = photo, 1 = video)	照片/视频标记（0 =照片，1 =视频）
def loadDataSet(fileName, splitChar='\t'):
    # 打开数据集
    inFile = open(fileName)
    dataSet  = {}
    
    # 读取原据集 infile
    for line in inFile:
        # 分割元数据
        meteData = line.strip().split(splitChar)
        # 将元数据存入字典，键是照片/视频标识符，值是元数据其他元素
        mapIndex = meteData[0]
        mapValue = meteData[1:]
        dataSet[mapIndex] = mapValue
        
    inFile.close()
    return dataSet 


# 计算pic之间的距离,根据经纬度获取实际距离
# param  照片的元数据，第2和第3个元素是经纬度信息
# return 两点间的距离(公里)
def distanceForPic(p1, p2):
    geolocator = Nominatim()
    pointA = (float(p1[3]), float(p1[2]))
    pointB = (float(p2[3]), float(p2[2]))
    return vincenty(pointA, pointB).miles


# 判断两个pic是否在eps范围内，即两点是否是邻居
# param  两个pic元数据a,b，距离eps
# return 是邻居返回1，否则返回0
def isNeighborInEps(a, b, eps):
    return distanceForPic(a, b) < eps


# 从全部数据集中查找point的邻居点
# param  数据集data，某点ID，距离eps
# return 某点的邻居点ID集合
def neighborQuery(data, pointId, eps):
    neighbos = []
    for inedx, value in data.items():
        if isNeighborInEps(data[pointId], data[inedx], eps):
            neighbos.append(inedx)
    return neighbos

# 能否成功分类？
# param  数据集, 分类结果, 待分类点id, 簇id, 半径大小, 最小点个数
# return 能否成功分类
def expandCluster(data, clusterResult, pointId, clusterId, eps, minPts):
    neighbos = neighborQuery(data, pointId, eps)
    
    # 不满足minPts条件的为噪声点
    if len(neighbos) < minPts:
        clusterResult[pointId] = NOISE
        return False
    # 划分到该簇
    else:
        clusterResult[pointId] = clusterId
        for seedId in neighbos:
            clusterResult[seedId] = clusterId
        
        # 持续扩张
        while len(neighbos) > 0:
            currentPoint = neighbos[0]
            queryResults = neighborQuery(data, currentPoint, eps)
            
            if len(queryResults) >= minPts:
                for i in range(len(queryResults)):
                    resultPoint = queryResults[i]
                    if clusterResult[resultPoint] == UNCLASSIFIED:
                        neighbos.append(resultPoint)
                        clusterResult[resultPoint] = clusterId
                        
                    elif clusterResult[resultPoint] == NOISE:
                        clusterResult[resultPoint] = clusterId
                        
            neighbos = neighbos[1:]
        return True


# DBSCAN 算法的实现
# param 数据集, 半径大小, 最小点个数
# return 分类簇id
def DBSCAN(data, eps, minPts):
    clusterCount = 1
    clusterResult = {}
    
    for inedx, value in data.items():
        clusterResult[inedx] = UNCLASSIFIED

    for inedx, value in data.items():
        point = data[inedx]
        if clusterResult[inedx] == UNCLASSIFIED:
            if expandCluster(data, clusterResult, inedx, clusterCount, eps, minPts):
                clusterCount = clusterCount + 1
    return clusterResult, clusterCount

def main():
    dataSet = loadDataSet('yfcc100m_dataset-0/temp.txt', '\t')
    clusters, clusterNum = DBSCAN(dataSet, 2, 15)
    
    outFile = open('yfcc100m_dataset-0/temp-clusters.txt', 'w')
    
    # 将同一个簇的pic_id放在一个集合里
    clusterResault = {}
    for pointId, clusterId in clusters.items():
        temp = []
        temp.append(pointId)
        clusterResault.setdefault(clusterId, temp)
        clusterResault[clusterId].append(pointId)
        
    #print(clusterResault)
    for index, value in clusterResault.items():
        newLine = '\t'.join(value)
        outFile.write(newLine + '\n')
    
    outFile.close()
    
if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print('finish all in %s' % str(end - start))
    plt.show()
        
    
    
    