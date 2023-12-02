from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib import admin


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название статьи")
    summary = models.CharField(max_length=255, verbose_name="Анонс")
    full_text = models.TextField(verbose_name="Полный текст")
    category = models.CharField(max_length=255, verbose_name="Категория")
    rubrica = models.CharField(max_length=255, null=True, blank=True)
    pubdate = models.DateTimeField(verbose_name="Дата публикации")
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="images", null=True, verbose_name="Фотографии")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_page", kwargs={"slug": self.slug})

    def get_category_url(self):
        return reverse("category_page", kwargs={"category": self.category})

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
