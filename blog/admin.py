from django.contrib import admin
from .models import Article


class ChoiceInline(admin.TabularInline):
    model = Article
    extra = 5


class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Date information", {"fields": ["pubdate"]}),
        ("Full_text", {"fields": ["full_text"]}),
        ("Category", {"fields": ["category"]}),
        ("Slug", {"fields": ["slug"]}),
        ("Image", {"fields": ["image"]}),
    ]
    list_display = ("title", "pubdate", "image", "category")
    list_filter = ["pubdate", "category"]
    search_fields = ["title"]

    """ Добавление функций в действие """

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

    """ Добавление функций в действие """


admin.site.register(Article, BlogAdmin)
