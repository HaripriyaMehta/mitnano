# -*- coding: utf-8 -*-

import argparse
import io
import re
import pandas as pd
from google.cloud import storage
from google.cloud import vision
from google.protobuf import json_format
import json
import requests
from PIL import Image, ImageDraw
import requests
from io import BytesIO



# [START def_detect_text]

# [START def_detect_text_uri]
def detect_document_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    var = "fifteen"
 #   client = storage.Client()
 #   bucket = client.bucket('mitlayers')
 #   pic = 126
    df = pd.DataFrame()
   # for blob in bucket.list_blobs(prefix=var):
   
    #print(blob.name)
    
 #   client = vision.ImageAnnotatorClient()
 #   image = vision.types.Image()
 #   image.source.image_uri = "https://storage.googleapis.com/mitlayers/two/Screen%20Shot%202018-09-15%20at%201.18.02%20PM.png"
    response = requests.get("https://storage.googleapis.com/mitlayers/two/Screen%20Shot%202018-09-15%20at%201.18.02%20PM.png")
    img = Image.open(BytesIO(response.content))
    #"gs://mitlayers/"+blob.name
 #   response = client.document_text_detection(image = image)
 #   texts = response.text_annotations

    draw = ImageDraw.Draw(img)
    x = 2201
    y = 1553
    a= 2263
    b =1563
    draw.rectangle([(x-1, y-1),(a+1,b+1) ], outline="red")
    draw.rectangle([(x-2, y-2),(a+2,b+2) ], outline="red")
    draw.rectangle([(x-3, y-3),(a+3,b+3) ], outline="red")

    img.show()
##    for i in range(len(texts)):
##        if i!=0:
##            a = texts[i].description
##            b = texts[i].bounding_poly.vertices[0].x
##            c = texts[i].bounding_poly.vertices[0].y
##            d = texts[i].bounding_poly.vertices[2].x
##            e = texts[i].bounding_poly.vertices[2].y
##            print([a,b,c,d,e])
##            df_new = pd.DataFrame([[a,b,c,d,e]])
##            df.append(df_new)
##    print(df)
    #df.to_csv("hackmit" + var + "fun.csv")


    

# [END vision_text_detection_gcs]

def run_uri(args):
    if args.command == 'document-uri':
        detect_document_uri(args.uri)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')
    
    document_uri_parser = subparsers.add_parser(
        'document-uri', help=detect_document_uri.__doc__)
    document_uri_parser.add_argument('uri')

    args = parser.parse_args()

    if 'uri' in args.command:
        run_uri(args)

