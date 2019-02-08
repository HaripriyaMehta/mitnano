import pandas as pd
import numpy as np
import requests
from PIL import Image, ImageDraw
import requests
from io import BytesIO
from django.http import HttpResponse

def search(names):
    # name, box number, line number
    df = pd.read_csv('./HACKmerged.csv', encoding = "ISO-8859-1")
    # x1, y1, x2, y2, box number
    df2 = pd.read_csv('./pixmerged.csv', encoding = "ISO-8859-1")
    # id, screenshot name
    df3 = pd.read_csv('./nameconversion.csv', encoding = "ISO-8859-1")

    # dictionary mapping name index to set of box, line tuples
    dicty={}
    dicty[0] = ()

    # name index
    counter = 0

    # convert names to uppercase
    names = [element.upper() for element in names]  
    for i in names:
        samebox = df.loc[df['name'] == i, 'boxNumber'].tolist()
        sameline = df.loc[df['name'] == i, 'lineNumber'].tolist()
        dicty[counter] = set(list(zip(samebox, sameline)))
        counter+=1

    ans = dicty[0].intersection(*dicty.values())

    perfectwork = []
    if len(names) == 2:
        dictyforpix = {}
        for j in list(ans):
            boxno = j[0]
            individualpixels = []
            dictyforpix[j] = {}
            for k in names:
                y1values = set(df2.loc[(df2['name'] == k) & (df2['boxno'] == str(boxno)), 'y1'].tolist())
                dictyforpix[j][k] = y1values
            y1values = dictyforpix[j][names[0]].intersection(*dictyforpix[j].values())
            perfectwork.append((list(y1values)[0], boxno))


        minimum = 10000
        value = 0;
        for each in perfectwork:
            firstx2 = df2.loc[(df2['name'] == names[0]) & (df2['y1'] == str(each[0])) & (df2['boxno'] == str(each[1])) , 'x2'].tolist()[0]
            secondx1 = df2.loc[(df2['name'] == names[1])  & (df2['y1'] == str(each[0])) & (df2['boxno'] == str(each[1])), 'x1'].tolist()[0]
            if (0< int(secondx1) - int(firstx2) < minimum):
                minimum = int(secondx1) - int(firstx2)
                value = each
        y1 = value[0]
        boxno = value[1]
        firstname = df2.loc[(df2['name'] == names[0])  & (df2['boxno'] == str(boxno)) & (df2['y1'] == y1), ['x1', 'x2', 'y2']]
        lastname = df2.loc[(df2['name'] == names[1]) & (df2['boxno'] == str(boxno)) & (df2['y1'] == y1), ['x1', 'x2', 'y2']]

        x1 = int(firstname['x1'].tolist()[0])
        x12 = int(lastname['x2'].tolist()[0])
        y2 = int(firstname['y2'].tolist()[0])
        y1 = int(y1)



        response = requests.get("https://storage.googleapis.com/mitlayers/"+ df3.loc[(df3['id'] == boxno), 'screenshot'].tolist()[0])
        img = Image.open(BytesIO(response.content))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(x1-1, y1-1),(x12+1,y2+1) ], outline="red")
        draw.rectangle([(x1-2, y1-2),(x12+2,y2+2) ], outline="red")
        draw.rectangle([(x1-3, y1-3),(x12+3,y2+3) ], outline="red")
        del draw
        # img.show()
        # We need an HttpResponse object with the correct mimetype
        response = HttpResponse(content_type="image/png")
        # now, we tell the image to save as a PNG to the 
        # provided file-like object
        img.save(response, 'PNG')

        return response

    else:
        try:
            boxno = list(ans)[0][0]
        except:
            return False
        else:
            x1 = int(df2.loc[(df2['name'] == names[0]) & (df2['boxno'] == str(boxno)), 'x1'].tolist()[0])
            x2 = int(df2.loc[(df2['name'] == names[0]) & (df2['boxno'] == str(boxno)), 'x2'].tolist()[0])
            y1 = int(df2.loc[(df2['name'] == names[0]) & (df2['boxno'] == str(boxno)), 'y1'].tolist()[0])
            y2 = int(df2.loc[(df2['name'] == names[0]) & (df2['boxno'] == str(boxno)), 'y2'].tolist()[0])
            response = requests.get("https://storage.googleapis.com/mitlayers/"+ df3.loc[(df3['id'] == boxno), 'screenshot'].tolist()[0])
            img = Image.open(BytesIO(response.content))
            draw = ImageDraw.Draw(img)
            draw.rectangle([(x1-1, y1-1),(x2+1,y2+1) ], outline="red")
            draw.rectangle([(x1-2, y1-2),(x2+2,y2+2) ], outline="red")
            draw.rectangle([(x1-3, y1-3),(x2+3,y2+3) ], outline="red")
            del draw
            response = HttpResponse(content_type="image/png")
            img.save(response, 'PNG')
            img.show()
            return response

                                
        
    
                                
