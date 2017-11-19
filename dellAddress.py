
# 将地址翻转，国家在最前
# @param fliename原始文件名
# @return none
def reserveAddress(fliename):
    # 打开数据集
    inFile = open(fliename,encoding='UTF-8')
    datas = []

    # 读取原数据集 infile
    for line in inFile:
        # 分割元数据
        meteData = line.strip().split('\t')
        datas.append(meteData)
    inFile.close()
    
    i = 0
    for i in range(len(datas)):
    #while i<10:
        address = datas[i][2].strip().split(', ')
        address.reverse()
        datas[i][2] = ', '.join(address)

    i = 0
    outFile = open(fliename, 'w', encoding='utf-8')
    for i in range(len(datas)):
        outFile.write(datas[i][0] + '\t' + datas[i][2] + '\n')
    outFile.close()


# 按省份分离信息
# @param fliename原始文件名
# @return none
def splitByProvince(fliename):
    provinces = ['河北省', '山西省', '内蒙古自治区', '黑龙江省', '吉林省', '辽宁省', '陕西省', \
                 '甘肃省', '青海省', '新疆维吾尔自治区', '宁夏回族自治区', '山东省', '河南省', \
                 '江苏省', '浙江省', '安徽省', '江西省', '福建省', '臺灣', '湖北省', '湖南省',\
                 '广东省', '广西壮族自治区', '海南省', '四川省', '云南省', '贵州省', '西藏自治区', \
                 '北京市', '上海市', '天津市', '重庆市', '澳門', 'HK']
                 
    # 打开数据集
    inFile = open(fliename, encoding='UTF-8')
    datas = []

    # 读取原数据集 infile
    for line in inFile:
        # 分割元数据
        meteData = line.strip().split('\t')
        datas.append(meteData)
    inFile.close()

    for i in range(len(datas)):
        flag = 0
        for j in range(len(provinces)):
            # 找到此条地址匹配的省份信息
            if(datas[i][1].find(provinces[j]) != -1):
                datas[i].append(provinces[j])
                flag = 1
        if(flag == 0):
            datas[i].append('None')

    outFile = open(fliename, 'w', encoding='utf-8')
    for i in range(len(datas)):
        outFile.write(datas[i][0] + '\t' + datas[i][2] + '\t' + datas[i][1] +'\n')
    outFile.close()

def readTest():
    baseDir = 'yfcc100m_dataset-3/'
    geoFile = baseDir + 'flick-3-geo-abortchina-china'
    addressFile = baseDir + 'flick-3-geo-abortchina-china-address'
    ##
    reserveAddress(addressFile)
    splitByProvince(addressFile)


readTest()

