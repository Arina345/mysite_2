from django.db import models
from datetime import datetime
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    full_text = models.TextField()
    category = models.CharField(max_length=255)
    rubrica = models.CharField(max_length=255, null=True, blank=True)
    pubdate = models.DateTimeField()
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="images", null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_page", kwargs={"slug": self.slug})

    def get_category_url(self):
        return reverse("category_page", kwargs={"category": self.category})
