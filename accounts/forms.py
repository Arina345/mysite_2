from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "email"]

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
        fields = ["first_name", "last_name", "email"]


# ProfileEditForm позволит пользователям редактировать данные профиля, сохраненные в конкретно-прикладной модели Profile.
# Пользователи смогут редактировать дату своего рождения и закачивать изоражение на сайт в качестве фотоснимка профиля.


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo", "blog_description"]
