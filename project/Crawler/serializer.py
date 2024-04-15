from rest_framework import serializers
from .models import CrawlingModel

class CrawlingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlingModel
        fields = ['title']