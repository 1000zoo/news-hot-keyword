from django.urls import path
from .views import CrawlingRouter

urlpatterns = [
    path('crawling/', CrawlingRouter.as_view()),
]