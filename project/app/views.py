from django.shortcuts import render
import json

test_data = {"Python": 5, "Java": 4, "C++": 3, "Django": 3, "Spring": 4}

# Create your views here.
def index(request):
    context = {"hotkeywords": test_data}
    return render(request, 'hotkeyword/index.html', context=context)

def chart(request):
    context = {"hotkeywords": json.dumps(test_data)}
    return render(request, 'hotkeyword/chart.html', context=context)