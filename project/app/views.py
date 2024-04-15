from django.shortcuts import render
import json
import requests
from django.utils import timezone
from datetime import timedelta

from .models import Hotkeywords

def load_data():
    # response = requests.post("http://127.0.0.1:8000/api/crawling/")
    hotkeywords = Hotkeywords.objects.all()[:10]
    results = {}
    for hotkeyword in hotkeywords:
        results[hotkeyword.keyword_text] = hotkeyword.count
        print(hotkeyword.keyword_date)
    return results

# Create your views here.
def index(request):
    lastest_keywords = load_data()
    context = {"hotkeywords": lastest_keywords}
    return render(request, 'hotkeyword/index.html', context=context)

def chart(request):
    lastest_keywords = load_data()
    context = {"hotkeywords": json.dumps(lastest_keywords)}
    return render(request, 'hotkeyword/chart.html', context=context)