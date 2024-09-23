from django.contrib import admin

# Register your models here.
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_registr", "photo"]
    raw_id_fields = ["user"]
