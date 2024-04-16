from django.shortcuts import render
import json
import requests
from django.utils import timezone
from datetime import timedelta

from .models import Hotkeywords

def get_today_keywords():
    return {"a":5, "b":2, "c":1, "d":10, "e":11, "f":12, "g": 1, "h": 4, "i":5, "j":6}

def get_latest_keywords():
    return Hotkeywords.objects.all().order_by("-keyword_date")[:10]

def sorted_dict(dictionary: dict):
    results = {}
    keys = sorted(dictionary.keys(), key=lambda k:dictionary[k])
    keys.reverse()
    for key in keys:
        results[key] = dictionary[key]
    return results

def load_data():
    hotkeywords = get_latest_keywords()
    results = {}
    for hotkeyword in hotkeywords:
        results[hotkeyword.keyword_text] = hotkeyword.count
    return sorted_dict(results)

# Create your views here.
def index(request):
    # response = requests.post("http://127.0.0.1:8000/api/crawling/")
    lastest_keywords = load_data()
    today_keywords = get_today_keywords()
    context = {"hotkeywords": lastest_keywords, "todaykeywords": today_keywords}
    return render(request, 'hotkeyword/index.html', context=context)

def chart(request, id):
    if id == 0:
        keywords = load_data()
    else:
        keywords = get_today_keywords()
    context = {"hotkeywords": json.dumps(keywords)}
    return render(request, 'hotkeyword/chart.html', context=context)
