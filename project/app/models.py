from django.db import models

# Create your models here.

class Hotkeywords(models.Model):
    keyword_text = models.CharField(max_length=200)
    keyword_date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.keyword_text
    

class Dailykeywords(models.Model):
    keyword_text = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
    keyword_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword_text
    
class Wordclouds(models.Model):
    wordcloud_date = models.DateTimeField(auto_now_add=True)
    wordcloud_img = models.ImageField(null=True, upload_to="hotkeyword")
