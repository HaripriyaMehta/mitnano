import pandas as pd
import numpy as np
import requests
from PIL import Image, ImageDraw
import requests
from io import BytesIO

def search(names):
    df = pd.read_csv('./picture/HACKmerged.csv', encoding = "ISO-8859-1")
    df2 = pd.read_csv('./picture/pixmerged.csv', encoding = "ISO-8859-1")
    df3 = pd.read_csv('./picture/nameconversion.csv', encoding = "ISO-8859-1")

    dicty={}
    dicty[0] = ()
    counter = 0

    

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

        img.show()


    else:
        boxno = list(zip(*ans))[0]
        for i in boxno:
            print(i)
            x1 = int(df2.loc[(df2['name'] == names[0]) & (df2['boxno'] == str(i)), 'x1'].tolist()[0])
            x2 = int(df2.loc[(df2['name'] == names[0]) & (df2['boxno'] == str(i)), 'x2'].tolist()[0])
            y1 = int(df2.loc[(df2['name'] == names[0]) & (df2['boxno'] == str(i)), 'y1'].tolist()[0])
            y2 = int(df2.loc[(df2['name'] == names[0]) & (df2['boxno'] == str(i)), 'y2'].tolist()[0])
            response = requests.get("https://storage.googleapis.com/mitlayers/"+ df3.loc[(df3['id'] == i), 'screenshot'].tolist()[0])
            img = Image.open(BytesIO(response.content))
            draw = ImageDraw.Draw(img)
            draw.rectangle([(x1-1, y1-1),(x2+1,y2+1) ], outline="red")
            draw.rectangle([(x1-2, y1-2),(x2+2,y2+2) ], outline="red")
            draw.rectangle([(x1-3, y1-3),(x2+3,y2+3) ], outline="red")
            img.show()


    

        
    
                                
