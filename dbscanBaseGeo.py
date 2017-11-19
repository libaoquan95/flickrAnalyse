import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
from sklearn import datasets

class DBSCAN(object):
    
    # 初始化类
    # param eps:邻域的距离阈值, 
    #       minPts:样本点要成为核心对象所需要的邻域的样本数阈值
    def __init__(self, eps, minPts):
        self.eps    = eps
        self.minPts = minPts
        self.UNCLASSIFIED = False
        self.NOISE = 0
    # 计算两点之间的距离,根据经纬度获取实际距离
    # param  p1, p2: 点经纬度信息，经度在前，纬度在后
    # return 两点间的距离(公里)
    def distanceForPoint(self, p1, p2):
        #geolocator = Nominatim()
        pointA = (float(p1[1]), float(p1[0]))
        pointB = (float(p2[1]), float(p2[0]))
        return vincenty(pointA, pointB).miles
    
    
    # 判断两个pic是否在eps范围内，即两点是否是邻居
    # param   p1, p2: 点经纬度信息，经度在前，纬度在后
    # return 是邻居返回1，否则返回0
    def isNeighbors(self, p1, p2):
        return self.distanceForPoint(p1, p2) < self.eps
    
       
    # 从全部数据集中查找point的邻居点
    # param  数据集data，某点ID，距离eps
    # return 某点的邻居点ID集合
    def neighborQuery(self, dataset, pointIndex):
        neighbos = []
        for inedx in range(len(dataset)):
            if self.isNeighbors(dataset[pointIndex], dataset[inedx]):
                neighbos.append(inedx)
        return neighbos
    
    # 能否成功分类？
    # param  数据集, 分类结果, 待分类点id, 簇id, 半径大小, 最小点个数
    # return 能否成功分类
    def expandCluster(self, dataset, clusterResult, pointIndex, clusterId):
        neighbos = self.neighborQuery(dataset, pointIndex)
        
        # 不满足minPts条件的为噪声点
        if len(neighbos) < self.minPts:
            clusterResult[pointIndex] = self.NOISE
            return False
        # 划分到该簇
        else:
            clusterResult[pointIndex] = clusterId
            for seedId in neighbos:
                clusterResult[seedId] = clusterId
            
            # 持续扩张
            while len(neighbos) > 0:
                currentPoint = neighbos[0]
                queryResults = self.neighborQuery(dataset, currentPoint)
                
                if len(queryResults) >= self.minPts:
                    for i in range(len(queryResults)):
                        resultPoint = queryResults[i]
                        if clusterResult[resultPoint] == self.UNCLASSIFIED:
                            neighbos.append(resultPoint)
                            clusterResult[resultPoint] = clusterId
                            
                        elif clusterResult[resultPoint] == self.NOISE:
                            clusterResult[resultPoint] = -1
                            
                neighbos = neighbos[1:]
            return True
    
    # DBSCAN 算法的实现
    # param 数据集
    # return 分类簇id
    def fit_predict(self, dataset):
        clusterCount = 1
        clusterResult = []
        
        for inedx in range(len(dataset)):
            clusterResult.append(self.UNCLASSIFIED)
            
        dataset = np.array(dataset).tolist()
    
        for inedx in range(len(dataset)):
            if clusterResult[inedx] == self.UNCLASSIFIED:
                if self.expandCluster(dataset, clusterResult, inedx, clusterCount):
                    clusterCount = clusterCount + 1
        
        return  np.array(clusterResult), clusterCount


    
    '''
if __name__ == '__main__':
    
    X = []
    
    DBSCANs = DBSCAN(eps=0.5, minPts=10)
    clusters, clusterNum = DBSCANs.fit_predict(X)
    clusters, clusterNum = DBSCAN(eps = 0.5, minPts = 10).fit_predict(proGeo)
    
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
    
    '''
    
    
    