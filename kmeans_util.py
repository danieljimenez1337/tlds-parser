import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class clusteredData():
    def __init__(self,dataSet)-> None:
        self.__dataSet = dataSet
        self.__centriods,self.__belongsTo = elbowMethod(dataSet,5)
        
    
    def plot(self) -> None:
        k = len(self.__centriods)
        colors = ['r', 'g','y']
        #color=iter(cm.rainbow(np.linspace(0,1,k)))
        __, ax = plt.subplots()

        for i in range(len(self.__dataSet)):
            x = self.__dataSet[i][0]
            y = self.__dataSet[i][1]
            ax.plot(x, y, (colors[int(self.__belongsTo[i])] + 'o'))
        
        for i in range(k):
            ax.plot(self.__centriods[i][0], self.__centriods[i][1], 'bo')
        plt.show()

    def getBelongsTo(self):
        return self.__belongsTo



def euclidian(a, b):
    return np.linalg.norm(a-b)

def kmeans(k: int, dataSet: np.array):
    numInstances, numFeatures = dataSet.shape

    # intializes the centriods at a random starting point
    startingIndexes = np.random.randint(0, numInstances - 1, size=k)
    centriods = dataSet[startingIndexes]

    oldCentriods = np.zeros(centriods.shape)
    belongsTo = np.zeros((numInstances, 1))
    norm = euclidian(centriods,oldCentriods)

    while norm > 0:
        norm = euclidian(centriods,oldCentriods)

        for  dataIndex, data in enumerate(dataSet):
            distanceToCentriod = np.zeros((k,1))
            for centriodIndex, centroid in enumerate(centriods):
                distanceToCentriod[centriodIndex] = euclidian(centroid,data)
            
            belongsTo[dataIndex][0] = np.argmin(distanceToCentriod)
        
        
        tmpCentriods = np.zeros((k, numFeatures))
        for index in range(len(centriods)):
            # data points assigned to cluster
            assignedData = [i for i in range(len(belongsTo)) if belongsTo[i] == index]
            centriod = np.mean(dataSet[assignedData], axis=0)
            tmpCentriods [index, :] = centriod
        
        oldCentriods = centriods
        centriods = tmpCentriods
    
    return centriods, belongsTo

def getLine(x1,y1,x2,y2):
    m =(y2-y1)/(x2-x1)
    b = y2 - (m*x2)
    return m,b

def getClusters(centriods, belongsTo, dataSet):
    clusters = []
    for centriod in centriods:
        cluster = {} 
        cluster["centriod"] = centriod
        cluster["dataPoints"] = []
        clusters.append(cluster)

    for itemIndex, item in enumerate(belongsTo):
        clusters[int(item)]["dataPoints"].append(dataSet[itemIndex])

    return clusters
    
        
        


def getClusterMean(cluster):
    distance = 0
    for datapoint in cluster["dataPoints"]:
        distance += euclidian(cluster["centriod"],datapoint)
    try:
        return distance/len(cluster["dataPoints"])
    except ZeroDivisionError:
        print("zero sized cluster")
        print(cluster)
        return 0
    

def plotElbowMethod(datas):
    #color=iter(cm.rainbow(np.linspace(0,1,k)))
    __, ax = plt.subplots()

    for dataIndex, data in enumerate(datas):
        x = dataIndex
        y = data["sse"]
        ax.plot(x, y, "bo")
    plt.show()

def elbowMethod(dataSet, maxK = 8):
    datas = []
    for i in range(1,maxK+1):
        data = {}
        centriods, belongsTo = kmeans(i,dataSet)
        data['centriods'] = centriods
        data['belongsTo'] = belongsTo
        data['sse'] = 0
        clusters = getClusters(centriods, belongsTo, dataSet)
        for cluster in clusters:
            mean = getClusterMean(cluster)
            for dataPoint in cluster["dataPoints"]:
                data['sse'] += (euclidian(dataPoint,cluster["centriod"]) - mean )**2
        datas.append(data)  
    plotElbowMethod(datas)
    m,b = getLine(0,datas[0]['sse'],len(datas)-1,datas[len(datas)-1]['sse'])
    best = 0
    length = 0

    for i in range(len(datas)):
        y = m*i +b
        print(y-datas[i]["sse"])
        if y - datas[i]["sse"] > length:
            best = i
            length = y - datas[i]["sse"]

    return datas[best]['centriods'], datas[best]['belongsTo']





