import json
from copy import deepcopy
import sys
import numpy as np
from typing import List

class BoundaryBox():
    def __init__(self,x: int,y: int,width: int,height: int) -> None: 
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

    def getX(self) -> int:
        return self.__x

    def getY(self) -> int:
        return self.__y
    
    def getWidth(self) -> int:
        return self.__width
    
    def getHeight(self) -> int:
        return self.__height
    

class Word(BoundaryBox):
    def __init__(self,text: str,x: int,y: int,width: int,height: int) -> None:
        super().__init__(x,y,width,height)
        self.__text = text

    def getText(self) -> str:
        return self.__text

class Line(BoundaryBox):
    def __init__(self,x: int,y: int,width: int,height: int) -> None:
        super().__init__(x,y,width,height)
        self.words = []
        self.__text=""
    
    def addText(self,text: str):
        if self.__text=="":
            self.__text += text
        else:
            self.__text += " " + text 

    def getText(self) -> str:
        return self.__text
    
    def getCharWidth(self)->float:
        return self.getWidth()/len(self.__text)


class Region(BoundaryBox):
    def __init__(self,x: int,y: int,width: int,height: int) -> None:
        super().__init__(x,y,width,height)
        self.lines = []

class Page():
    def __init__(self,language: str,textAngle: float,orientation:str) -> None:
        self.regions=[]
        self.__language = language
        self.__textAngle = textAngle
        self.__orientation = orientation
    
    def getLanguage(self) -> str:
        return self.__language

    def getTextAngle(self) -> float:
        return self.__textAngle

    def getOrientation(self) -> str:
        return self.__orientation
        

class ParsedImage():
    
    def __init__(self,jsonFileName:str) -> None:
        self.pages = convertJson(jsonFileName)
    
    def printPages(self):
        for page in self.pages:
            for region in page.regions:
                for line in region.lines:
                    print(line.getText())
    
    def getText(self):
        paragraphs = []
        paragraph =[]
        for page in self.pages:
            for region in page.regions:
                for line in region.lines:
                    if lineIsIndented(region,line):
                        paragraphs.append(paragraph)
                        paragraph = [line.getText()]
                    else:
                        paragraph.append(line.getText())
        
        paragraphs.append(paragraph)
        return {"paragraphs":paragraphs}

def percentError(actual: float, expected: float) -> float:
    return abs((actual-expected)/expected)*100

def lineIsIndented(region ,line)->bool: 
    diff = abs(region.getX() - line.getX())
    cW = line.getCharWidth()
    if diff > 3* cW and diff < 6*cW:
        return True
    else:
        return False
                    

def convertBB(BoundaryBox) -> (int,int,int,int):  
    bb = list(BoundaryBox.split(","))
    x =  int(bb[0])
    y =  int(bb[1])
    width =  int(bb[2])
    height =  int(bb[3])
    return (x,y,width,height)

def convertJson(jsonFileName:str) -> List[Page]:

    with open(jsonFileName) as json_data:
        data = (json.load(json_data))

    pages=[]
    for page in data["pages"]:
        language = page["language"]
        textAngle= float(page["textAngle"])
        orientation = page["orientation"]
        pageObject= Page(language,textAngle,orientation)
        pages.append(pageObject)
        for region in page['regions']:
            x,y,width,height = convertBB(region["boundingBox"])
            regionObject = Region(x,y,width,height)
            pageObject.regions.append(regionObject)
            for line in region["lines"]:
                x,y,width,height = convertBB(line["boundingBox"])
                lineObject = Line(x,y,width,height)
                regionObject.lines.append(lineObject)
                for word in line["words"]:
                    x,y,width,height = convertBB(word["boundingBox"])
                    wordObject = Word(word["text"],x,y,width,height)
                    lineObject.words.append(wordObject)
                    lineObject.addText(wordObject.getText())
    return pages

def convertDataForKmeans(pages: List[Page]) -> np.ndarray:
    dataset=[]
    for page in pages:    
        for region in page.regions:
                for line in region.lines:
                    templist = []
                    lineaveragewidth = 0
                    lineaverageheight = 0
                    charctercount = 0
                    for word in line.words:
                        lineaveragewidth += word.width
                        lineaverageheight += word.height
                        charctercount += len(word.text)

                    templist.append(lineaveragewidth/charctercount)
                    templist.append(lineaverageheight/len(line.words))
                    dataset.append(templist)
    return np.array(dataset)


def main():
    if len(sys.argv)==3:
        pi = ParsedImage(sys.argv[1])
        output = pi.getText()
        with open(sys.argv[2],'w') as fp:
            json.dump(output,fp)
    else:
        print("Please Enter two arguments, json file, name of output")

if __name__ == "__main__":
    main()

