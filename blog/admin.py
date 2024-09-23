from django.contrib import admin
from .models import Article
from django.utils.safestring import mark_safe
from django.contrib import messages


class ChoiceInline(admin.TabularInline):
    model = Article

    # fieldsets = [
    #     (None, {"fields": ["title"]}),
    #     ("Автор", {"fields": ["author"]}),
    #     ("Дата публикации", {"fields": ["pubdate"]}),
    #     ("Краткое содержание", {"fields": ["summary"]}),
    #     ("Полный текст", {"fields": ["full_text"]}),
    #     ("Slug", {"fields": ["slug"]}),
    #     ("Фото", {"fields": ["image"]}),
    # ]


class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    # фильтр
    list_filter = ["status", "publish", "author"]
    search_fields = ["title", "full_text"]
    # автоматическое заполнение slug
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]


admin.site.register(Article, BlogAdmin)


# from .models import Profile


# # Чтобы профиль появидся в базах данных
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ["user", "date_registr", "photo"]
#     raw_id_fields = ["user"]
