from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib import admin
from django.utils import timezone


class Article(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=500, verbose_name="Название статьи")
    summary = models.CharField(max_length=255, verbose_name="Анонс")
    full_text = models.TextField(verbose_name="Полный текст")
    category = models.CharField(max_length=255, verbose_name="Категория")
    rubrica = models.CharField(max_length=255, null=True, blank=True)
    pubdate = models.DateTimeField(verbose_name="Дата публикации")
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="images", null=True, verbose_name="Фотографии")
    is_published = models.BooleanField(
        choices=Status.choices, default=Status.DRAFT, verbose_name="Статус"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_page", kwargs={"slug": self.slug})

    def get_category_url(self):
        return reverse("category_page", kwargs={"category": self.category})

    class Meta:
        verbose_name = "Статьи"
        verbose_name_plural = "Статьи"
