import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#import pandas as pd
#import seaborn as sns
from mpl_toolkits.basemap import Basemap
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon

# 画出中国地图，并将数据集中的经纬点在图中标记
# @param filename:数据集，lonIndex:经度下标，latIndex:维度下标
def drawMap(filename,  lonIndex,  latIndex):
    inFile = open(filename)
    datas = []
    lon = []
    lat = []
    # 读取原数据集 infile
    for line in inFile:
        # 分割元数据
        meteData = line.strip().split('\t')
        datas.append(meteData)
        lon.append(float(meteData[lonIndex]))
        lat.append(float(meteData[latIndex]))
    
    fig = plt.gcf()
    
    map = Basemap(projection='stere',  
                  lat_0=35,  
                  lon_0=110, 
                  llcrnrlon=82.33,  
                  llcrnrlat=3.01,  
                  urcrnrlon=138.16,  
                  urcrnrlat=53.123, 
                  resolution='l', 
                  area_thresh=10000, 
                  rsphere=6371200.)
    
    # CHN_adm1的数据是中国各省区域
    shp_info = map.readshapefile("CHN_adm_shp/CHN_adm1", 'states', drawbounds=True)

    #map.drawmapboundary()   # 绘制边界
    #map.fillcontinents()    # 填充大陆，发现填充之后无法显示散点图，应该是被覆盖了
    #map.drawstates()        # 绘制州
    #map.drawcoastlines()    # 绘制海岸线
    #map.drawcountries()     # 绘制国家
    #map.drawcounties()      # 绘制县
    
    fig.set_size_inches(30,  30)

    parallels = np.arange(0., 90, 10.) 
    map.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10) # 绘制纬线
    
    meridians = np.arange(80., 140., 10.)
    map.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10) # 绘制经线
    
    
    x, y = map(lon, lat)
    
    # map.scatter(x, y, edgecolors='r', facecolors='r', marker='*', s=320)
    
    map.scatter(x, y, s=10)
    
    plt.title("flick point in China")
    
    fig.savefig('yfcc100m_dataset/China.png',  dpi=100)
    #plt.show()
    
    inFile.close()
    
    
drawMap('yfcc100m_dataset/flick-geo-abortchina-china', 10, 11)