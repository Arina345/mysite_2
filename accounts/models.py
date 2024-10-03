from django.db import models
from django.conf import settings


# Профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # blank=True поле необязательное и его можно оставить пустым
    date_registr = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(
        upload_to="images", verbose_name="Фотография", blank=True, null=True
    )
    blog_description = models.TextField(
        max_length=250, blank=True, verbose_name="Описание блога"
    )

    def __str__(self):
        return f"Profile of {self.user.username}"
