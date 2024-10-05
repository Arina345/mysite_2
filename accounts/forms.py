from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "Пароль"}),
    )
    password2 = forms.CharField(
        label="Повтор пароля",
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Повтор пароля"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "input", "placeholder": "Имя пользователя без пробела"}
            ),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "Email"}),
        }

    # Валидация полей, чтобы проверить, что оба пароля одинаковы.
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]


# UserEditForm позволит пользователям редактировать свое имя, фамилию и адрес электронной почты,
# которые являются атрибутами встроенной в Django модели User;


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "input", "placeholder": "Имя пользователя"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "input", "placeholder": "Email пользователя"}
            ),
        }


# ProfileEditForm позволит пользователям редактировать данные профиля, сохраненные в конкретно-прикладной модели Profile.
# Пользователи смогут редактировать дату своего рождения и закачивать изоражение на сайт в качестве фотоснимка профиля.

from django.forms import ClearableFileInput


class MyClearableFileInput(ClearableFileInput):
    template_name = "accounts/custom_clearable_file_input.html"
    initial_text = ""
    input_text = ""


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo", "blog_description"]
        widgets = {
            "blog_description": forms.Textarea(
                attrs={"class": "input", "placeholder": "О блоге"}
            ),
            "photo": MyClearableFileInput(
                attrs={
                    "template_name": "accounts/custom_clearable_file_input.html",
                    "class": "photo_input",
                }
            ),
        }
