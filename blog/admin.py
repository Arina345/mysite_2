from django.contrib import admin
from .models import Article
from django.utils.safestring import mark_safe
from django.contrib import messages


class ChoiceInline(admin.TabularInline):
    model = Article


class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Дата публикации", {"fields": ["pubdate"]}),
        ("Краткое содержание", {"fields": ["summary"]}),
        ("Полный текст", {"fields": ["full_text"]}),
        ("Категория", {"fields": ["category"]}),
        ("Slug", {"fields": ["slug"]}),
        ("Фото", {"fields": ["image"]}),
        ("Статус", {"fields": ["is_published"]}),
    ]
    list_display = ("title", "pubdate", "image", "category")

    list_filter = ["pubdate", "category", "is_published"]
    search_fields = ["title"]
    search_help_text = "Найти по названию статьи"
    view_on_site = True

    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")

    list_display = ("title", "pubdate", "get_html_photo", "category")
    get_html_photo.short_description = "Фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Article.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Article.Status.DRAFT)
        self.message_user(
            request, f"{count} записи(ей) сняты с публикации!", messages.WARNING
        )

    actions = ["set_published", "set_draft"]


admin.site.register(Article, BlogAdmin)
