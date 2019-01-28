import json
import argparse
import numpy as np

from copy import deepcopy
from typing import List

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image


class BoundingBox():
    def __init__(self, rawBoundingBox: dict) -> None:
        boundingDimension = rawBoundingBox["boundingBox"]
        bb = list(boundingDimension.split(","))
        self.__x = int(bb[0])
        self.__y = int(bb[1])
        self.__width = int(bb[2])
        self.__height = int(bb[3])
    
    def __eq__(self,other):
        if self.getX() == other.getX() and self.getY() == other.getY():
            return True
        else:
            return False

    def __ne__(self,other):
        if self == other:
            return False
        else:
            return True
    
    def getX(self) -> int:
        return self.__x

    def getY(self) -> int:
        return self.__y

    def getWidth(self) -> int:
        return self.__width

    def getHeight(self) -> int:
        return self.__height


class enlargedBB():
    def __init__(self,BB: BoundingBox)-> None:
        if BB.getWidth() >= BB.getHeight():
            self.__x = int(round(BB.getX() - (BB.getWidth()/8)))
            self.__y = int(round(BB.getY() - (BB.getHeight()/2)))
            self.__width = int(round(BB.getWidth() + (BB.getWidth()/4)))
            self.__height = int(round(BB.getHeight() + (BB.getHeight()/2)))
        else:
            self.__x = int(round(BB.getX() - (BB.getWidth()/2)))
            self.__y = int(round(BB.getY() - (BB.getHeight()/2)))
            self.__width = int(round(BB.getWidth() + (BB.getWidth())))
            self.__height = int(round(BB.getHeight() + (BB.getHeight())))
    
    def getX(self) -> int:
        return self.__x

    def getY(self) -> int:
        return self.__y

    def getWidth(self) -> int:
        return self.__width

    def getHeight(self) -> int:
        return self.__height

class Word(BoundingBox):
    def __init__(self, rawWord: dict) -> None:
        super().__init__(rawWord)
        self.__text = rawWord["text"]

    def getText(self) -> str:
        return self.__text


class Line(BoundingBox):
    def __init__(self, rawLine: dict) -> None:
        super().__init__(rawLine)
        self.__words = []
        self.__text = ""
        self.isolated = True
        self.__enlargedBB = enlargedBB(self)

        for word in rawLine["words"]:
            wordObject = Word(word)
            self.__words.append(wordObject)
            self.addText(wordObject.getText())

    def addText(self, text: str) -> None:
        if self.__text == "":
            self.__text += text
        else:
            self.__text += " " + text

    def getText(self) -> str:
        return self.__text

    def getCharWidth(self) -> float:
        return self.getWidth()/len(self.__text)

    def getWords(self) -> List[Word]:
        return self.__words
    
    def getEnlargedBB(self):
        return self.__enlargedBB



class Region(BoundingBox):
    def __init__(self, rawRegion: dict) -> None:
        super().__init__(rawRegion)
        self.__lines = []

        for line in rawRegion["lines"]:
            self.__lines.append(Line(line))

    def getLines(self) -> List[Line]:
        return self.__lines


class Page():
    def __init__(self, rawPage: dict) -> None:
        self.__regions = []
        self.__language = rawPage["language"]
        self.__textAngle = float(rawPage["textAngle"])
        self.__orientation = rawPage["orientation"]

        for region in rawPage['regions']:
            self.__regions.append(Region(region))

    def getLanguage(self) -> str:
        return self.__language

    def getTextAngle(self) -> float:
        return self.__textAngle

    def getOrientation(self) -> str:
        return self.__orientation

    def getRegions(self) -> List[Region]:
        return self.__regions


class ParsedImage():

    def __init__(self, jsonFileName: str) -> None:
        self.__pages = []

        with open(jsonFileName) as jsonData:
            data = (json.load(jsonData))
            for page in data["pages"]:
                self.__pages.append(Page(page))
        self.checkIsolation()
        #self.displayLines("./testdata/test-image.jpg", enlarged=True)

    def printPages(self) -> None:
        for page in self.__pages:
            for region in page.getRegions():
                for line in region.getLines():
                    print(line.getText())

    def getPages(self) -> List[Page]:
        return self.__pages

    def displayLines(self,imageFileName, enlarged = False):
        plt.figure(figsize=(8,9))
        image  = Image.open(imageFileName)
        ax     = plt.imshow(image, alpha=0.5)
        for page in self.__pages:
            for region in page.getRegions():
                for line in region.getLines():
                    if enlarged:
                        bb = line.getEnlargedBB()
                    else:
                        bb = line

                    origin = (bb.getX(), bb.getY())
                    patch  = Rectangle(origin, bb.getWidth(), bb.getHeight(), fill=False, linewidth=1, color='b')
                    ax.axes.add_patch(patch)

        _ = plt.axis("off")
        plt.show()

    def getText(self) -> dict:
        paragraphs = []
        paragraph = ""
        hypen = False
        for page in self.__pages:
            for region in page.getRegions():
                for line in region.getLines():
                    if  not line.isolated:
                        lineTxt = line.getText()
                        if lineIsIndented(region, line):
                            hypen = False
                            paragraphs.append(paragraph)
                            if lineTxt[len(lineTxt)-1] == "-":
                                paragraph = lineTxt[:-1]
                                hypen = True
                            else:
                                paragraph = lineTxt
                        else:
                            if not hypen:
                                lineTxt = " " + lineTxt
                            else:
                                hypen = False

                            if lineTxt[len(lineTxt)-1] == "-":
                                paragraph += lineTxt[:-1]
                                hypen = True
                            else:
                                paragraph += lineTxt
                        

        paragraphs.append(paragraph)
        return {"paragraphs": paragraphs}

    def checkIsolation(self):
        for page1 in self.getPages():
            for region1 in page1.getRegions():
                for line1 in region1.getLines():
                    for page2 in self.getPages():
                        for region2 in page2.getRegions():
                            for line2 in region2.getLines():
                                if (line1 != line2 and checkBoundingBoxCollision(line1.getEnlargedBB(),line2.getEnlargedBB()) ):
                                    line1.isolated = False
                            
                                    

def percentError(actual: float, expected: float) -> float:
    return abs((actual-expected)/expected)*100


def lineIsIndented(region, line)->bool:
    diff = abs(region.getX() - line.getX())
    cW = line.getCharWidth()
    if diff > 3 * cW and diff < 6*cW:
        return True
    else:
        return False


def checkBoundingBoxCollision(box1: BoundingBox, box2: BoundingBox)->bool:
    b1W = box1.getWidth()
    b1H = box1.getHeight()
    b1X = box1.getX()
    b1Y = box1.getY()

    b2W = box2.getWidth()
    b2H = box2.getHeight()
    b2X = box2.getX()
    b2Y = box2.getY()

    if ((b1X < (b2X + b2W)) and ((b1X + b1W) > b2X) and (b1Y < (b2Y + b2H)) and ((b1Y + b1H) > b2Y)):
        return True
    else:
        return False


def convertDataForKmeans(pages: List[Page]) -> np.ndarray:
    dataset = []
    for page in pages:
        for region in page.getRegions():
                for line in region.getLines():
                    tempList = []
                    lineAverageWidth = 0
                    lineAverageHeight = 0
                    characterCount = 0
                    for word in line.getWords():
                        lineAverageWidth += word.width
                        lineAverageHeight += word.height
                        characterCount += len(word.text)

                    tempList.append(lineAverageWidth/characterCount)
                    tempList.append(lineAverageHeight/len(line.getWords()))
                    dataset.append(tempList)
    return np.array(dataset)


def main():
    parser = argparse.ArgumentParser(description='OCR Parser for Lemillion')
    parser.add_argument(
        'inputJSON', help='input json file full path', type=str)
    parser.add_argument(
        'outputJSON', help='output json file full path', type=str)
    args = parser.parse_args()

    pi = ParsedImage(args.inputJSON)
    output = pi.getText()
    with open(args.outputJSON, 'w') as fp:
        json.dump(output, fp)

if __name__ == "__main__":
    main()
