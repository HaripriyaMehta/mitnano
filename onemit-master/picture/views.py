from .dataread import search
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.generic.list import ListView

import operator

from django.db.models import Q
from .models import Entry
from functools import reduce



def index(request):
    # return HttpResponse("Hello, world. You're at the pictures index. You should be seeing a picture")
    return render(request, 'base.html')

def process(request):
    return render(request, 'process.html')

def team(request):
    return render(request, 'team.html')

def community(request):
    return render(request, 'community.html')

import pandas as pd
import numpy as np

# name, box number, line number
df = pd.read_csv('./picture/HACKmerged.csv', encoding = "ISO-8859-1")
# x1, y1, x2, y2, box number
df2 = pd.read_csv('./picture/pixmerged.csv', encoding = "ISO-8859-1")
# id, screenshot name
df3 = pd.read_csv('./picture/nameconversion.csv', encoding = "ISO-8859-1")

def searchHighlightedBoxName(names):
    dicty={}
    dicty[0] = ()
    counter = 0
    for i in names:
        # converting i to upper case
        i = i.upper()
        samebox = df.loc[df['name'] == i, 'boxNumber'].tolist()
        sameline = df.loc[df['name'] == i, 'lineNumber'].tolist()
        dicty[counter] = set(list(zip(samebox, sameline)))
        counter+=1

    ans = dicty[0].intersection(*dicty.values())
    return (list(ans))

def results(request):
    context['image_name']
    return render (request, 'result_list.html')

class ResultListView(ListView):
    """
    Display a Blog List page filtered by the search query.
    """
    paginate_by = 10
    model= Entry
    template_name='result_list.html'

    def get_queryset(self):
        # result = super(ResultListView, self).get_queryset()
        result= Entry.objects.all()
        # print(result.count())

        query = self.request.GET.get('q')
        # result_list=[]
        # box_line_list=[]
        if query:
            query_list = query.split()
            return searchHighlightedBoxName(query_list)[0]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        # context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context = {}
        context['queryset'] = self.get_queryset()
        mapping = {}
        i = 0
        for y in range(15):
            for x in range(9):
                mapping[i] = str(i) + '.png'
                i += 1
        context['first']= context['queryset']
        context['image_name']= mapping[int(context['queryset'][0])]
        context['text_name']= df3.loc[df['id'] == int(context['queryset'][0])+1, 'screenshot'].tolist()[0]
        print(context['text_name'])
        return context

