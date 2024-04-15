from django.db import models

# Create your models here.

class Hotkeywords(models.Model):
    keyword_text = models.CharField(max_length=200)
    keyword_date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.keyword_text