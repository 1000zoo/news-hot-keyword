from . import views
from django.urls import path, include

app_name = "hotkeywords"
urlpatterns = [
    path('', views.index, name="index"),
    path('chart/', views.chart, name='chart')
]