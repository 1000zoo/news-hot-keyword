from django.shortcuts import render
import json
import requests
from django.utils import timezone
from datetime import timedelta

from .models import Hotkeywords

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
    response = requests.post("http://127.0.0.1:8000/api/crawling/")
    hotkeywords = get_latest_keywords()
    results = {}
    for hotkeyword in hotkeywords:
        results[hotkeyword.keyword_text] = hotkeyword.count
    return sorted_dict(results)

# Create your views here.
def index(request):
    lastest_keywords = load_data()
    context = {"hotkeywords": lastest_keywords}
    return render(request, 'hotkeyword/index.html', context=context)

def chart(request):
    lastest_keywords = load_data()
    context = {"hotkeywords": json.dumps(lastest_keywords)}
    return render(request, 'hotkeyword/chart.html', context=context)
