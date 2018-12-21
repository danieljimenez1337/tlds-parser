import requests
from io import BytesIO
import json
import sys

if len(sys.argv)==3:
    subscription_key = "39de83d6c6d64fb1a83404740a53e404"
    assert subscription_key

    #vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
    
    vision_base_url = "https://westus.api.cognitive.microsoft.com/vision/v2.0/"
    ocr_url = vision_base_url + "ocr"

    image_path = str(sys.argv[1])

    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
    params  = {'language': 'unk', 'detectOrientation': 'true'}

    response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    data = response.json()

    with open(str(sys.argv[2]), 'w') as outfile:
        json.dump(data, outfile)
else:
    print("Please Enter Two arguments, name of image, name of output")