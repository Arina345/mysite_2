from django.db import models
from datetime import datetime


class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    full_text = models.TextField()
    category = models.TextField(max_length=255)
    pubdate = models.DateTimeField()
    slug = models.CharField(max_length=255, unique=True)
    # is_published = models.BooleanField() #TODO

    def __str__(self):
        return self.title
