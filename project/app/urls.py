from . import views
from django.urls import path, include

app_name = "hotkeywords"
urlpatterns = [
    path('<int:id>/', views.index, name="index"),
    path('chart/<int:id>/', views.chart, name='chart')
]