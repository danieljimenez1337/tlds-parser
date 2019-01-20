import json
import argparse
import sys
import numpy as np

from copy import deepcopy
from typing import List


class BoundingBox():
    def __init__(self, rawBoundingBox: dict) -> None:
        boundingDimension = rawBoundingBox["boundingBox"]
        bb = list(boundingDimension.split(","))
        self.__x = int(bb[0])
        self.__y = int(bb[1])
        self.__width = int(bb[2])
        self.__height = int(bb[3])

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

    def printPages(self) -> None:
        for page in self.__pages:
            for region in page.getRegions():
                for line in region.getLines():
                    print(line.getText())

    def getPages(self) -> List[Page]:
        return self.__pages

    def getText(self) -> dict:
        paragraphs = []
        paragraph = []
        for page in self.__pages:
            for region in page.getRegions():
                for line in region.getLines():
                    if lineIsIndented(region, line):
                        paragraphs.append(paragraph)
                        paragraph = [line.getText()]
                    else:
                        paragraph.append(line.getText())

        paragraphs.append(paragraph)
        return {"paragraphs": paragraphs}


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
