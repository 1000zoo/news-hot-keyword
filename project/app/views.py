from django.shortcuts import render
import json

# Create your views here.
def index(request):
    test_data = {"Python": 5, "Java": 4, "C++": 3, "Django": 3, "Spring": 4}
    context = {"hotkeywords": test_data}
    return render(request, 'hotkeyword/index.html', context=context)
