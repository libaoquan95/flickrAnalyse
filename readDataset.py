from operator import itemgetter, attrgetter
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import sys

#原始数据集格式
#	 [0]	Photo/video identifier	照片/视频标识符
#	 [1]	User NSID	用户NSID
#	 [2]	User nickname	用户昵称
#	 [3]	Date taken	拍摄日期
#	 [4]	Date uploaded	上传日期
#	 [5]	Capture device	捕获设备
#	 [6]	Title	标题
#	 [7]	Description	描述
#	 [8]	User tags (comma-separated)	用户标签（逗号分隔）
#	 [9]	Machine tags (comma-separated)	机器标签（逗号分隔）
#	[10]	Longitude	经度
#	[11]	Latitude	纬度
#	[12]	Accuracy	准确性
#	[13]	Photo/video page URL	照片/视频页面URL
#	[14]	Photo/video download URL	照片/视频下载网址
#	[15]	License name	许可证名称
#	[16]	License URL	许可网址
#	[17]	Photo/video server identifier	照片/视频服务器标识符
#	[18]	Photo/video farm identifier	照片/视频农场标识符
#	[19]	Photo/video secret	照片/视频秘密
#	[20]	Photo/video secret original	照片/视频秘密原件
#	[21]	Extension of the original photo	扩展原始照片
#	[22]	Photos/video marker (0 = photo, 1 = video)	照片/视频标记（0 =照片，1 =视频）


# 从原始数据集中提取带有geo标签的数据
# @param fliename原始文件名
# @return none
def getGeoDataFromDataset(fliename):
    # 打开数据集
    inFile = open(fliename)
    outFile = open(fliename + '-geo', 'w')
    
    i = 0
    count = 0
    # 读取原数据集 infile
    for line in inFile:
        # 分割元数据
        meteData = line.strip().split('\t')
        
        # 此照片或视频带有geo信息
        if(meteData[10] != '' and meteData[11] != ''):
            outFile.write(line)
            count = count + 1
        
        if(i % 1000000 == 0):
            print ('处理了 %d 行, geo有 %d 行' % (i, count))
        
        i = i + 1
            
    print ('共 %d 行, geo共 %d 行' % (i, count))
    
    inFile.close()
    outFile.close()
    
   
# 从带有geo标签的数据集中提取出geo大概在中国范围内的数据
# 最东端 东经135度2分30秒 黑龙江和乌苏里江交汇处 
# 最西端 东经73度40分 帕米尔高原乌兹别里山口（乌恰县） 
# 最南端 北纬3度52分 南沙群岛曾母暗沙 
# 最北端 北纬53度33分 漠河以北黑龙江主航道（漠河)
# 转换后
# 经：   73.66667  -  135.04167
# 纬：   3.86667  -  53.55
# @param fliename原始文件名
# @return none
def getAbortChinaFromGeoData(fliename):
    # 打开数据集
    inFile = open(fliename)
    outFile = open(fliename + '-abortchina', 'w')
    
    i = 0
    count = 0
    # 读取原数据集 infile
    for line in inFile:
        # 分割元数据
        meteData = line.strip().split('\t')
        
        # 此geo信息位于中国
        if(float(meteData[10]) >= 73.66667 and float(meteData[10]) <= 135.04167 and \
           float(meteData[11]) >= 3.86667  and float(meteData[11]) <= 53.55):
            newLine = '\t'.join(meteData)
            outFile.write(newLine + '\n')
            count = count + 1
        
        if(i % 1000000 == 0):
            print ('处理了 %d 行, 中国geo有 %d 行' % (i, count))
        
        i = i + 1
            
    print ('共 %d 行, 中国geo共 %d 行' % (i, count))
    
    inFile.close()
    outFile.close()
    
    
# 简化数据集信息，元数据仅包含信息如下：
# 数据集格式
#	 [0] [0]	Photo/video identifier	照片/视频标识符
#	 [1] [1]	User NSID	用户NSID
#	 [3] [2]	Date taken	拍摄日期
#	[10] [3]	Longitude	经度
#	[11] [4]	Latitude	纬度
#	[13] [5]	Photo/video page URL	照片/视频页面URL
#	[22] [6]	Photos/video marker (0 = photo, 1 = video)	照片/视频标记（0 =照片，1 =视频）
# @param fliename原始文件名
# @return none
def simpleDataset(fliename):
    # 打开数据集
    # 打开数据集
    inFile = open(fliename)
    outFile = open(fliename + '-simple', 'w')
    count = 0
    colIndex = [0,1,3,10,11,13,22]
    
    # 读取原数据集 infile
    for line in inFile:
        # 分割元数据
        meteData = line.strip().split('\t')
        
        newLine = '\t'.join(meteData[i] for i in colIndex)
        outFile.write(newLine + '\n')
        
        if(count % 1000000 == 0):
            print ('处理了 %d 行' % count)
        
        count = count + 1
            
    print ('共 %d 行' % count)
    
    inFile.close()
    outFile.close()
    
  
# 从带有geo标签的数据集中提取出geo实际在中国范围内的数据
# 通过Geopy，有经纬度获取实际地址
# geopy的函数参数是纬度在前，经度在后
# @param fliename原始文件名，lonIndex经度下标，latIndex维度下标,操作次数n
# @return none
def getChinaFromDatasetByGeopy(filename, lonIndex, latIndex, n=10):
    # 打开数据集
    inFile = open(filename)
    datas = []
    isFinsih = []
    
    # 读取原数据集 infile
    for line in inFile:
        # 分割元数据
        meteData = line.strip().split('\t')
        datas.append(meteData)
        isFinsih.append(0)
    inFile.close()
    
    
    inFile = open(filename, 'w', encoding='utf-8')
    outFile = open(filename + '-china-address', 'a', encoding='utf-8')
    outFile2 = open(filename + '-china', 'a', encoding='utf-8')
    
    # 逐条获取数据的实际地址
    # 若地址位于中国，将信息写入新文件
    # 将未处理的数据重新写入到原文件
    geolocator = Nominatim()
    
    i = 0
    count = 0
    error_count = 0
    none_count = 0
    while i<n and i<len(datas):
        try:
            # 根据经纬坐标获取实际地址
            location = geolocator.reverse("" + datas[i][latIndex] +"," +  datas[i][lonIndex])
            if (location.address != None):
                addressArr = location.address.split(',')
                country = addressArr[len(addressArr)-1].strip()
                # 标记已处理
                isFinsih[i] = 1
                # 地址位于中国
                if(country in ["中国","臺灣"]):
                    outFile.write(datas[i][0] + '\t' +  country + '\t' + location.address + '\n')
                    outFile2.write('\t'.join(datas[i]) + '\n')
                    count += 1
            else:
                none_count += 1
                isFinsih[i] = 2
        except GeocoderTimedOut as e:
            #print('tiom out: ' + datas[i][0])
            error_count += 1

        i += 1
        sys.stdout.write('处理 %d 行, 中国 %d 行，请求超时 %d 行，none %d 行\r' % (i, count, error_count, none_count))
        sys.stdout.flush()
        #if(i % 10 == 0):
        #    print ('处理 %d 行, 中国 %d 行，请求超时 %d 行，none %d 行' % (i, count, error_count, none_count))
    print('')
    
    # 重新写入未处理数据
    length = len(isFinsih)
    for i in range(length):
        if(isFinsih[i] == 0):
            inFile.write('\t'.join(datas[i]) + '\n')
            
    for i in range(length):
        if(isFinsih[i] == 2):
            inFile.write('\t'.join(datas[i]) + '\n')
    
    inFile.close()
    outFile.close()
    outFile2.close()
    
    
def readTest():
    baseDir = 'yfcc100m_dataset-3/'
    
    #getGeoDataFromDataset(baseDir + 'flick-3')
    #getAbortChinaFromGeoData(baseDir + 'flick-3-geo') 
    
    count = input("input: ")
    getChinaFromDatasetByGeopy(baseDir + 'flick-3-geo-abortchina',\
                               10, 11, int(count))



readTest()

