import argparse
import io
import re
import pandas as pd
from google.cloud import storage
from google.cloud import vision
from google.protobuf import json_format
import json
import requests 

def detect_document_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    var = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "forteen", "fifteen"] 
    client = storage.Client()
    bucket = client.bucket('mitlayers')
    listy = []
    for i in var:
        pic = 0
        for blob in bucket.list_blobs(prefix=i):
            listy.append([blob.name])
            pic+=1
    df = pd.DataFrame(listy, columns =['screenshot'])
    df.to_csv("nameconversion.csv")
    
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


