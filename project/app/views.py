from django.shortcuts import render
import json
import requests
from django.utils import timezone
from datetime import timedelta

from .models import Hotkeywords, Dailykeywords

def home(request): #변경
    return render(request, 'home.html')

## views
def index(request):
    # response = requests.post("http://127.0.0.1:8000/api/crawling/")
    hotkeywords = load_data(get_hotkeywrods())
    dailykeywords = load_data(get_dailykeywords())
    context = {"hotkeywords": hotkeywords, "todaykeywords": dailykeywords}
    return render(request, 'hotkeyword/index.html', context=context)

def chart(request, id):
    if id == 0:
        keywords = get_hotkeywrods()
        title = "실시간 키워드"
    else:
        keywords = get_dailykeywords()
        title = "오늘의 키워드"
    context = {"hotkeywords": json.dumps(load_data(keywords)), "chart_title": title}
    return render(request, 'hotkeyword/chart.html', context=context)

## utils
def get_dailykeywords():
    return Dailykeywords.objects.all().order_by("-count")[:10]

def get_hotkeywrods():
    return Hotkeywords.objects.all().order_by("-keyword_date")[:10]

def load_data(keywords):
    results = {}
    for keyword in keywords:
        results[keyword.keyword_text] = keyword.count
    return sorted_dict(results)

def sorted_dict(dictionary: dict):
    results = {}
    keys = sorted(dictionary.keys(), key=lambda k:dictionary[k])
    keys.reverse()
    for key in keys:
        results[key] = dictionary[key]
    return results
