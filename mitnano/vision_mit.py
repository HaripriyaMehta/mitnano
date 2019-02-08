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

# [START def_detect_text]

# [START def_detect_text_uri]
def detect_document_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    var = "fifteen"
    client = storage.Client()
    bucket = client.bucket('mitlayers')
    pic = 126
    df = pd.DataFrame()
    for blob in bucket.list_blobs(prefix=var):
        print(blob.name)
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = "gs://mitlayers/"+blob.name
        response = client.document_text_detection(image=image)
        texts = response.text_annotations
        try:
            alllines = texts[0].description
            eachword = alllines.split("\n")
            for i in range(len(eachword)):
                newword = eachword[i].split()
                df_new = pd.DataFrame(newword, [i]*len(newword))
                df_new[1] = [pic]*len(newword)
                df = df.append(df_new)
        except:
            pass
        pic+=1
    df = df.sort_values(0)
    df.to_csv("hackmit" + var + ".csv")


    

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

