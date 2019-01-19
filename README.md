# Lemillion-Parser

This is a Optical Character Regcognition Parser using Microsoft Computer Vision APi. This will remove extrenous information from a
document.

## Getting Started

Some of files will require Matplotlib for plotting the data.

## Input file
### pages
An array of dictionaries, where each dict is a file returned by  Microsoft Computer Vision APi OCR.

### Example
```
  {
     "pages":[
        {
           "language":"en",
           "textAngle":-2.0000000000000338,
           "orientation":"Up",
           "regions":[
              {
                 "boundingBox":"462,379,497,258",
                 "lines":[
                    {
                       "boundingBox":"462,379,497,74",
                       "words":[
                          {
                             "boundingBox":"462,379,41,73",
                             "text":"A"
                          },
                          {
                             "boundingBox":"523,379,153,73",
                             "text":"GOAL"
                          },
                          {
                             "boundingBox":"694,379,265,74",
                             "text":"WITHOUT"
                          }
                       ]
                    },
                    {
                       "boundingBox":"565,471,289,74",
                       "words":[
                          {
                             "boundingBox":"565,471,41,73",
                             "text":"A"
                          },
                          {
                             "boundingBox":"626,471,150,73",
                             "text":"PLAN"
                          },
                          {
                             "boundingBox":"801,472,53,73",
                             "text":"IS"
                          }
                       ]
                    },
                    {
                       "boundingBox":"519,563,375,74",
                       "words":[
                          {
                             "boundingBox":"519,563,149,74",
                             "text":"JUST"
                          },
                          {
                             "boundingBox":"683,564,41,72",
                             "text":"A"
                          },
                          {
                             "boundingBox":"741,564,153,73",
                             "text":"WISH"
                          }
                       ]
                    }
                 ]
              }
           ]
        }
     ]
  }
```

## Output file
### paragraphs

An array of paragraphs represented by array of lines. 

### Example
```
{
   "paragraphs":[
      [
         "displayed a willingness to subjugate outsiders\u2014first",
         "Indians, who were nearly annihilated through war and",
         "disease, and then Africans, who were brought in chains",
         "to serve as slave labor, especially on the tobacco, rice,",
         "and indigo plantations of the southern colonies."
      ],
      [
         "But if the settlement experience gave people a com-",
         "mon stock of values, both good and bad, it also divided",
         "them. The thirteen colonies were quite different from",
         "one another. Puritans carved tight, pious, and relatively",
         "democratic communities of small family farms out of",
         "rocky-soiled New England. Theirs was a homogeneous",
         "world in comparison to most of the southern colonies,",
         "where large landholders, mostly Anglicans, built plan-",
         "tations along the coast from which they lorded over a",
         "labor force of black slaves and looked down upon the",
         "poor white farmers who settled the backcountry. Differ-",
         "ent still were the middle colonies stretching from New",
         "York to Delaware. There diversity reigned. Well-to-do",
         "merchants put their stamp on New York City, as Quak-",
         "ers did on Philadelphia, while out in the countryside",
         "sprawling estates were interspersed with modest home-",
         "steads. Within individual colonies, conflicts festered",
         "over economic interests, ethnic rivalries, and religious",
         "practices. All those clashes made it difficult for colo-",
         "nists to imagine that they were a single people with a",
         "common destiny, much less that they ought to break",
         "free from Britain."
      ]
   ]
}
```
### How to use

As of right now there only one working feature. This is called  using the parser_util file. You give the name and path of the json you wish to import Then the name and path of the ouput file.

```
python parser_util.py .\testdata\data.json .\outputs\out.json
```
