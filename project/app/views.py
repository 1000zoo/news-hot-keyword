from django.conf import settings
from django.shortcuts import render
import json
import requests
from django.utils import timezone
from datetime import timedelta
from .models import Hotkeywords, Dailykeywords, Wordclouds

import os

def home(request): #변경
    return render(request, 'home.html')

## views
def index(request, id):
    if id == 0:
        keywords = load_data(get_dailykeywords())
        title = "오늘의 키워드"
    else:
        response = requests.post("http://127.0.0.1:8000/api/crawling/")
        keywords = load_data(get_hotkeywrods())
        title = "실시간 키워드"

    context = {"hotkeywords": keywords, "title": title, "id": id}
    return render(request, 'hotkeyword/index.html', context=context)

def chart(request, id):
    img_path = get_image_path()
    if id == 0:
        keywords = get_dailykeywords()
        title = "오늘의 키워드"
    else:
        keywords = get_hotkeywrods()
        title = "실시간 키워드"
    context = {"hotkeywords": json.dumps(load_data(keywords)), "title": title, "wordcloud_path": img_path}
    return render(request, 'hotkeyword/chart.html', context=context)

## utils
def get_dailykeywords():
    return Dailykeywords.objects.filter(keyword_date__date=timezone.now().date()).order_by("-count")[:10]

def get_hotkeywrods():
    return Hotkeywords.objects.all().order_by("-keyword_date")[:10]

def get_image_path():
    wordcloud = Wordclouds.objects.filter(wordcloud_date__date=timezone.now().date()).first()
    return os.path.join(settings.MEDIA_ROOT, wordcloud.wordcloud_img.url)

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
