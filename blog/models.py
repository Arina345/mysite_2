from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.models import User


my_timezone = timezone.now()


class PublishedManager(models.Manager):
    def get_queryset(self):
        # возвращает опубликованные статьи
        # get_queryset() равносильно SELECT
        return super().get_queryset().filter(status=Article.Status.PUBLISHED)


class Article(models.Model):
    # Менеджер моделей - это класс, который действует как интерфейс,
    # через который модели Django взаимодействуют с базой данных.

    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=500, verbose_name="Название статьи")
    summary = models.CharField(max_length=500, verbose_name="Анонс")
    slug = models.CharField(max_length=255, unique=True)
    # Это поле определяет взаимосвязь многиек-одному, означающую,
    # что каждый пост написан пользователем и пользователь может написать любое число постов.

    # Параметр on_delete определяет поведение, которое следует применять
    # при удалении объекта, на который есть ссылка. Это поведение не относится конкретно к Django; оно является стандартным для SQL. Использование
    # ключевого слова CASCADE указывает на то, что при удалении пользователя, на
    # которого есть ссылка, база данных также удалит все связанные с ним посты в блоге.

    # Такой подход позволит легко обращаться к связанным объектам из
    # объекта User, используя обозначение user.article_posts.

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="article_posts"
    )
    full_text = models.TextField(verbose_name="Полный текст")
    publish = models.DateTimeField(default=my_timezone, verbose_name="Дата публикации")
    image = models.ImageField(
        upload_to="images", null=True, verbose_name="Фотографии", blank=True
    )
    update = models.DateTimeField(auto_now=True, verbose_name="Последнее обнавление")

    # default - значение по умолчанию
    # Status.choices это ссылка на набор вариантов,
    # определенных в другом месте кода, вероятно, в отдельном Status классе или перечислении.
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def get_absolute_url(self):
        return reverse("blog:article_detail", args=[self.slug])
