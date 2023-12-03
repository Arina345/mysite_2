from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Галлерея"
        verbose_name_plural = "Галлерея"
