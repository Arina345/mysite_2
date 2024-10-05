from django import forms
from .models import Article

from django.forms import ClearableFileInput


class MyClearableFileInput(ClearableFileInput):
    template_name = "accounts/custom_clearable_file_input.html"
    initial_text = ""
    input_text = ""


class EditArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "slug", "summary", "status", "full_text", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "input", "placeholder": "Введите название статьи"}
            ),
            "slug": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Введите название URL на англйиском языке",
                }
            ),
            "summary": forms.Textarea(
                attrs={
                    "class": "input",
                    "placeholder": "Введите краткое описание статьи",
                }
            ),
            "full_text": forms.Textarea(
                attrs={
                    "class": "input",
                    "placeholder": "Введите полный текст статьи",
                }
            ),
            "image": MyClearableFileInput(
                attrs={
                    "template_name": "accounts/custom_clearable_file_input.html",
                    "class": "photo_input",
                }
            ),
        }
