#-*- coding: utf-8 -*-
'''
Created on 2015-06-22
@author: Lockvictor
'''
import sys
import random
import math
import os
from operator import itemgetter


random.seed(0)


class ItemBasedCF(object):
    ''' TopN recommendation - Item Based Collaborative Filtering '''

    def __init__(self):
        self.trainset = {}        # 训练集
        self.testset = {}         # 测试集

        self.nSimAttraction = 20  # 最大相似景点数
        self.nRecAttraction = 10  # 推荐景点数

        self.attractionSimMatrix = {}   # 景点相似矩阵
        self.attractionPopular = {}     # 景点流行度
        self.attractionCount = 0        # 景点数量
        self.maxPhotoCount = 0          # 最大的照片数量

        #print('Similar attraction number = %d' % self.nSimAttraction, file=sys.stderr)
        #print('Recommended attraction number = %d' % self.nRecAttraction, file=sys.stderr)

    @staticmethod
    def loadfile(filename):
        ''' load a file, return a generator. '''
        fp = open(filename, 'r')
        
        for i, line in enumerate(fp):
            yield line.strip('\r\n')
            #if i % 100000 == 0:
                #print ('loading %s(%s)' % (filename, i), file=sys.stderr)
        fp.close()
        #print ('load %s succ' % filename, file=sys.stderr)

    def generateDataset(self, filename, pivot=0.7):
        ''' 加载数据集，分割为测试集和训练集'''
        trainset_len = 0
        testset_len = 0
        i = 0
        for line in self.loadfile(filename):
            userId, attractionId, photoCount = line.split(',')
            if(i == 0): #去除csv头
                i = 1
                continue
            self.maxPhotoCount = max(self.maxPhotoCount, int(photoCount))
            # 按pivot比例分割数据集
            if random.random() < pivot:
                self.trainset.setdefault(userId, {})
                self.trainset[userId][attractionId] = int(photoCount)
                trainset_len += 1
            else:
                self.testset.setdefault(userId, {})
                self.testset[userId][attractionId] = int(photoCount)
                testset_len += 1

        #print ('split training set and test set succ', file=sys.stderr)
        #print ('train set = %s' % trainset_len, file=sys.stderr)
        #print ('test set = %s' % testset_len, file=sys.stderr)
        #print(self.trainset)

    def calculateAttractionSim(self):
        ''' 计算景点的相似度矩阵 '''

        for userId, attractions in self.trainset.items():
            for attraction in attractions:
                # 计算项目流行度
                if attraction not in self.attractionPopular:
                    self.attractionPopular[attraction] = 0
                self.attractionPopular[attraction] += 1
        #print(self.attractionPopular)
        print('获取景点数目和流行度完成', file=sys.stderr)

        # 获取景点总数
        self.attractionCount = len(self.attractionPopular)

        # 计算景点相似度
        itemsim_mat = self.attractionSimMatrix
        for userId, attractions in self.trainset.items():
            for a1 in attractions:
                for a2 in attractions:
                    if a1 == a2:
                        continue
                    itemsim_mat.setdefault(a1, {})
                    itemsim_mat[a1].setdefault(a2, 0)
                    itemsim_mat[a1][a2] += 1

        # 计算景点相似度矩阵
        simfactor_count = 0
        PRINT_STEP = 2000000

        for a1, relatedAttraction in itemsim_mat.items():
            for a2, count in relatedAttraction.items():
                itemsim_mat[a1][a2] = count / math.sqrt(
                    self.attractionPopular[a1] * self.attractionPopular[a2])
                simfactor_count += 1
                if simfactor_count % PRINT_STEP == 0:
                    print('calculating attriction similarity factor(%d)' \
                          % simfactor_count, file=sys.stderr)

        print('计算景点相似度矩阵完成', file=sys.stderr)
        #print('Total similarity factor number = %d' % simfactor_count, file=sys.stderr)

    def recommend(self, user):
        ''' Find K similar attrictions and recommend N attrictions. '''
        K = self.nSimAttraction
        N = self.nRecAttraction
        rank = {}
        watched_attrictions = self.trainset[user]
        try:
            for attriction, rating in watched_attrictions.items():
                for related_attriction, similarity_factor in sorted(self.attractionSimMatrix[attriction].items(),
                                                               key=itemgetter(1), reverse=True)[:K]:
                    if related_attriction in watched_attrictions:
                        continue
                    rank.setdefault(related_attriction, 0)
                    rank[related_attriction] += similarity_factor * rating
        except KeyError:
            #print ('catch an exception')
            c = 1
            
        # return the N best attrictions
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]

    def evaluate(self):
        ''' 显示评估结果: precision, recall, coverage and popularity '''
        
        print('开始评估...', file=sys.stderr)

        N = self.nRecAttraction
        
        #  varables for precision and recall
        hit = 0
        rec_count = 0
        test_count = 0
        
        # varables for coverage
        all_rec_attractions = set()
        
        # varables for popularity
        popular_sum = 0

        for i, user in enumerate(self.trainset):
            if i % 500 == 0:
                print ('recommended for %d users' % i, file=sys.stderr)
            test_attrictions = self.testset.get(user, {})
            rec_attrictions = self.recommend(user)
            for attriction, _ in rec_attrictions:
                if attriction in test_attrictions:
                    hit += 1
                all_rec_attractions.add(attriction)
                popular_sum += math.log(1 + self.attractionPopular[attriction])
            rec_count += N
            test_count += len(test_attrictions)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_attractions) / (1.0 * self.attractionCount)
        popularity = popular_sum / (1.0 * rec_count)

        print ('precision=%.4f\trecall=%.4f\tcoverage=%.4f\tpopularity=%.4f' %
               (precision, recall, coverage, popularity), file=sys.stderr)


if __name__ == '__main__':
    
    baseDir = 'yfcc100m_dataset/'
    userAttractionFile = baseDir + 'user-attraction.csv' 
    
    #ratingfile = os.path.join('../dataset/ml-100k', 'u.data')
    
    itemcf = ItemBasedCF()
    itemcf.generateDataset(userAttractionFile)
    itemcf.calculateAttractionSim()
    itemcf.evaluate()