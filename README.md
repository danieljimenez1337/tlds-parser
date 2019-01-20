# Lemillion-Parser

This is an Optical Character Regcognition Parser written in **Python 3** using Microsoft Computer Vision API. This will remove extraneous information from a document, parse it for information, and return it in a json format ready to be used by the other components.

## Dependencies

Can be installed using pip:

- Matplotlib: for plotting data

## How to use

As of right now there is only one working feature. This is called using the parser_util file. You give the name and path of the json you wish to import, then the name and path of the ouput file.

```python
# change path format if on Windows
python3 parser_util.py ./testdata/data.json ./outputs/out.json
```

### Input file

The input file will be a json containing an array of dictionaries, where each dict is a file returned by Microsoft Computer Vision OCR service and represent the raw content of users' photos. The array need to have the same order as the users' inputs. The dict needs to contain information about languages, orientation, text angle, these info can be obtained by setting the correct parameters in the POST request for the Microsoft Service.

#### Example

```json
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

### Output file

The output json file will contain an array of paragraphs, each paragraph is represented by an array of lines, each line represented by a string.

#### Example

```json
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