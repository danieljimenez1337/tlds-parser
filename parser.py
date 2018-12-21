import json
from copy import deepcopy
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

jsonFileName = "testdata/data.json"

#This is the threshold for text that are similar sizes  
pixelDiferenceThreshold = 5

def convert(string): 
    li = list(string.split(",")) 
    return li

def boxHeight(data):
    boundingBox = convert(data["boundingBox"])
    return int(boundingBox[3]) 

def boxWidth(data):
    boundingBox = convert(data["boundingBox"])
    return int(boundingBox[2])

def boxXPos(data):
    boundingBox = convert(data["boundingBox"])
    return int(boundingBox[0])

def boxYPos(data):
    boundingBox = convert(data["boundingBox"])
    return int(boundingBox[1])

def getBoxList(data):
    return convert(data)
    
def averageWordHeight(data):

    total = 0
    count = 0
    for region in data["regions"]:
        for line in region["lines"]:
            for word in line["words"]:
                total += boxHeight(word)
                count += 1

    return total/count

def averageWordWidth(data):
    total = 0
    count = 0

    for region in data["regions"]:
        for line in region["lines"]:
            for word in line["words"]:
                total += boxWidth(word)
                count += 1

    return total/count

def averageSpaceWidth(data):
    total = 0
    count = 0

    for region in data["regions"]:
        for line in region["lines"]:
            wordCount =  len(line["words"])
            for i in range(wordCount-1):
                total += boxXPos(line["words"][i+1]) - (boxXPos(line["words"][i]) + boxWidth(line["words"][i])) 
                count += 1

    return total/count

                                     
def averageCharacterWidth(data):
    total = 0
    wordCount = 0
    for region in data["regions"]:
        for line in region["lines"]:
            wordCount +=  len(line["words"])
            for word in line["words"]:
                characterCount = len(word["text"])
                width = boxWidth(word)
                total += width/characterCount

    return total/wordCount

def checkBoundaryBoxCollision(box1,box2):
    b1W = boxWidth(box1)
    b1H = boxHeight(box1)
    b1X = boxXPos(box1)
    b1Y = boxYPos(box1) 

    b2W = boxWidth(box2)
    b2H = boxHeight(box2)
    b2X = boxXPos(box2)
    b2Y = boxYPos(box2)
        

    if ((b1X < (b2X + b2W)) and ((b1X + b1W) > b2X) and (b1Y < (b2Y + b2H)) and ((b1Y + b1H) > b2Y)):
        return True
    else:
        return False

def isLineIsolated(checkLine,data):
    checkLineX = boxXPos(checkLine)
    checkLineY = boxYPos(checkLine)
    for region in data["regions"]:
        for line in region["lines"]:
            lineX = boxXPos(line)
            lineY = boxYPos(line)
            #checks if same line
            if not (checkLineX == lineX and checkLineY == lineY):
                for word1 in line["words"]:
                    for word2 in checkLine["words"]:
                            if checkBoundaryBoxCollision(word2, word1):
                                return False
    return True
    
def getLineText(line):
    text = ""
    for word in line["words"]:
        text += word["text"]
        text += " " 
    return text

# puts the text into sections and puts those sections as strings in a list
def sectionizer(data):
    sections = []
    section = ""
    pastLine = None
    for line in data["regions"]["lines"]:
        if pastLine == None:
            section += line["text"]
            pastLine = line
        else:
            pass

    return sections

def lineIsIndented(region,line):
    rX = boxXPos(region)
    wX = boxXPos(line["words"][0]) 
    result =  (rX + pixelDiferenceThreshold) < wX
    return result

def printByRegion(data):
    rc = 1
    for region in data["regions"]:
        print("Region "+str(rc))
        for line in region["lines"]:
            linetxt = ""
            if (lineIsIndented(region,line)):
                linetxt += "\t"
            
            for word in line["words"]:
                linetxt += word["text"]
                linetxt += " " 
            print(linetxt)
        rc+=1
        print("--------------------------")

def printedIsolatedLines(data):
    for region in data["regions"]:
        for line in region["lines"]:
            if isLineIsolated(line,data):
                print(getLineText(line))

def plotLineBoxes(data,fileImageName):
    #show line boxes
    plt.figure(figsize=(8,9))

    image  = Image.open(fileImageName)
    ax     = plt.imshow(image, alpha=0.5)
    for region in data["regions"]:
        for line in region["lines"]:
            bbox = [int(num) for num in line["boundingBox"].split(",")]
            origin = (bbox[0], bbox[1])
            patch  = Rectangle(origin, bbox[2], bbox[3], fill=False, linewidth=1, color='y')
            ax.axes.add_patch(patch)
            #text = getLineText(line)
            #plt.text(origin[0], origin[1], text, fontsize=8, weight="bold", va="top")
    _ = plt.axis("off") 
    plt.show()

def plotRegionBoxes(data,fileImageName):
    plt.figure(figsize=(8,9))
    image  = Image.open(fileImageName)
    ax     = plt.imshow(image, alpha=0.5)
    for region in data["regions"]:
        bbox = [int(num) for num in region["boundingBox"].split(",")]
        origin = (bbox[0], bbox[1])
        patch  = Rectangle(origin, bbox[2], bbox[3], fill=False, linewidth=1, color='y')
        ax.axes.add_patch(patch)
    _ = plt.axis("off")
    plt.show()

def plotWordBoxes(data,fileImageName):
    plt.figure(figsize=(8,9))

    image  = Image.open(fileImageName)
    ax     = plt.imshow(image, alpha=0.5)

    for region in data["regions"]:
        for line in region["lines"]:
            for word in line["words"]:
                bbox = [int(num) for num in word["boundingBox"].split(",")]
                origin = (bbox[0], bbox[1])
                patch  = Rectangle(origin, bbox[2], bbox[3], fill=False, linewidth=1, color='b')
                ax.axes.add_patch(patch)
    _ = plt.axis("off")
    plt.show()

#this fuction enlarges word boxes
def enlargeWordBoxes(data):
    newdata = deepcopy(data)
    for region in newdata["regions"]:
        for line in region["lines"]:
            for word in line["words"]:
                b1W = boxWidth(word)
                b1H = boxHeight(word)
                b1X = boxXPos(word)
                b1Y = boxYPos(word)
                if b1W>b1H:
                    b1X = int(round(b1X - (b1W/4)))
                    b1Y = int(round(b1Y - (b1H/2)))
                    b1W = int(round(b1W +(b1W*0.5)))
                    b1H = int(round(b1H +(b1H)))
                else:
                    b1X = int(round(b1X - (b1W/2)))
                    b1Y = int(round(b1Y - (b1H/4)))
                    b1W = int(round(b1W +(b1W)))
                    b1H = int(round(b1H +(b1H*0.5)))
                word["boundingBox"] = str(b1X)+","+str(b1Y)+","+str(b1W)+","+str(b1H)
            
    return newdata

#opening the test json file 
with open(jsonFileName) as json_data:
    data = json.load(json_data)

newdata = enlargeWordBoxes(data)
plotWordBoxes(data,"testdata/test-image.jpg")
#printedIsolatedLines(newdata)



