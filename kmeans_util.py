import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class clusteredData():
    def __init__(self,dataSet)-> None:
        self.__dataSet = dataSet
        self.__centriods,self.__belongsTo = kmeans(2,dataSet)
    
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
    centriods = dataSet[np.random.randint(0, numInstances - 1, size=k)]

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
    
    return centriods ,belongsTo

