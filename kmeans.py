import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def euclidian(a, b):
    return np.linalg.norm(a-b)

def convert(string): 
    li = list(string.split(",")) 
    return li
def getLineText(line):
    text = ""
    for word in line["words"]:
        text += word["text"]
        text += " " 
    return text
def kmeans(k,dataset):
    history_centroids = []
    
    num_instances, num_features = dataset.shape
    
    
    prototypes = dataset[np.random.randint(0, num_instances - 1, size=k)]
    
    history_centroids.append(prototypes)
    
    prototypes_old = np.zeros(prototypes.shape)
    belongs_to = np.zeros((num_instances, 1))
    norm = euclidian(prototypes, prototypes_old)
    iteration = 0
    
    while norm > 0:
        iteration += 1
        print("interation: "+str(iteration))
        print("norm: "+str(norm))
        norm = euclidian(prototypes, prototypes_old)
        #for each instance in the dataset
        for index_instance, instance in enumerate(dataset):
            #define a distance vector of size k
            dist_vec = np.zeros((k,1))
            #for each centroid
            for index_prototype, prototype in enumerate(prototypes):
                #compute the distance between x and centroid
                dist_vec[index_prototype] = euclidian(prototype, instance)
            #find the smallest distance, assign that distance to a cluster
            belongs_to[index_instance][0] = np.argmin(dist_vec)
        tmp_prototypes = np.zeros((k, num_features))
        
        #for each cluster (k of them)
        for index in range(len(prototypes)):
            #get all the points assigned to a cluster
            instances_close = [i for i in range(len(belongs_to)) if belongs_to[i] == index]
            #find the mean of those points, this is our new centroid
            prototype = np.mean(dataset[instances_close], axis=0)
            #add our new centroid to our new temporary list
            tmp_prototypes[index, :] = prototype
        
        #set the new list to the current list
        prototypes_old = prototypes
        prototypes = tmp_prototypes
        
        #add our calculated centroids to our history for plotting
        history_centroids.append(tmp_prototypes)

    #return calculated centroids, history of them all, and assignments for which cluster each datapoint belongs to
    return prototypes, history_centroids, belongs_to

def plot(dataset, history_centroids, belongs_to):
    colors = ['r', 'g','y']

    #split our graph by its axis and actual plot
    fig, ax = plt.subplots()

    #for each point in our dataset
    for index in range(dataset.shape[0]):
        #get all the points assigned to a cluster
        instances_close = [i for i in range(len(belongs_to)) if belongs_to[i] == index]
        #assign each datapoint in that cluster a color and plot it
        for instance_index in instances_close:
            ax.plot(dataset[instance_index][0], dataset[instance_index][1], (colors[index] + 'o'))

    #lets also log the history of centroids calculated via training
    history_points = []
    #for each centroid ever calculated
    for index, centroids in enumerate(history_centroids):
        #print them all out
        for inner, item in enumerate(centroids):
            if index == 0:
                history_points.append(ax.plot(item[0], item[1], 'bo')[0])
            else:
                history_points[inner].set_data(item[0], item[1])
                print("centroids {} {}".format(index, item))

                plt.show()

def execute(dataset,data):
    
    centroids, history_centroids, belongs_to = kmeans(2,dataset)
    #plot the results
    #plot(dataset, history_centroids, belongs_to)
    count = 0 
    for page in data["pages"]:
        for region in page["regions"]:
                for line in region["lines"]:
                    line.cluster=belongs_to[count]
                    count +=1
                    
                    

jsonFileName = "testdata/data.json"
with open(jsonFileName) as json_data:
    data = json.load(json_data)

dataset = []    
for page in data["pages"]:
    for region in page["regions"]:
            for line in region["lines"]:
                templist = []
                lineaveragewidth = 0
                charctercount = 0
                linebox =  convert(line["boundingBox"])
                for word in line["words"]:
                    wordbox = convert(word["boundingBox"])
                    lineaveragewidth += int(wordbox[2])
                    charctercount += len(word["text"])
                templist.append(lineaveragewidth/charctercount)
                templist.append(int(linebox[3]))
                dataset.append(templist)

dataset = np.array(dataset)
print("executing")
execute(dataset,data)
                