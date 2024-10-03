from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
)
from django.contrib import messages

from blog.models import Article
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound


# обработка входа пользователя
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")

    # не отправлен запрос POST
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


# Мы добавили в него декоратор login_required, поскольку только аутентифицированные пользователи могут
# редактировать свои профили.


def dashboard(request, username=None):
    # Если username передан
    if username:
        # Функция попытается получить объект пользователя из базы данных
        try:
            user = User.objects.get(username=username)
        # Если пользователь не найден, функция вернет ошибку 404 с сообщением "Пользователь не найден".
        except User.DoesNotExist:
            return HttpResponseNotFound("Пользователь не найден")
    # Если пользователь найден, функция попытается получить профиль пользователя из базы данных
    else:
        user = request.user
    try:
        profile = Profile.objects.get(user=user)
    # Если профиль не найден, функция установит profile в None.
    except Profile.DoesNotExist:
        profile = None
    # Функция отфильтрует статьи, автором которых является текущий пользователь
    articles = Article.objects.filter(author=user)
    return render(
        request,
        "accounts/dashboard.html",
        {"user": user, "profile": profile, "articles": articles},
    )


@login_required
def edit(request):
    profile = Profile.objects.get(user=request.user)
    # Когда пользователь отправляет форму,то происходит следующее:
    if request.method == "POST":

        # Создает экземпляры UserEditForm и ProfileEditForm с данными текущего пользователя
        # и профиля соответственно и связывает данные формы из запроса (request.POST и request.FILES для загрузки файлов).

        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )

        # Проверяет, действительны ли обе формы валидны с помощью is_valid() метода.
        # Если действительны обе формы валидны, изменения сохраняются в моделях пользователя и профиля с помощью save() метода.
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль успешно обнавлен")
        else:
            messages.error(request, "Не удалось обновить профиль")

    #  Когда пользователь изначально загружает страницу (т.е. request.method != "POST"), код выполняет следующее:
    else:
        # Создает экземпляры UserEditForm и ProfileEditForm
        # с данными текущего пользователя и профиля соответственно, но без привязки каких-либо данных формы.
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    # Функция отрисовывает account/edit.html шаблон, который, как ожидается, будет отображать формы для редактирования пользователем информации своего профиля. Шаблон получит экземпляры
    # user_form и profile_form в качестве переменных, которые можно использовать для отображения форм и их полей.
    return render(
        request,
        "accounts/edit.html",
        {"user_form": user_form, "profile_form": profile_form, "profile": profile},
    )


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя,
            # но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            new_user.set_password(user_form.cleaned_data["password"])
            # Сохранить объект User
            new_user.save()

            # Создать профиль пользователя
            # При регистрации пользователей в системе будет создаваться объект Profile,
            # который будет ассоциирован с созданным объектом User.
            # ---------------------------------------------------------------------------------------------------
            # Изменено accounts/register_done.html на accounts/dashboard.html
            Profile.objects.create(user=new_user)
            form = LoginForm()
            return render(
                request,
                "accounts/register_done.html",
                {"new_user": new_user, "form": form},
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"user_form": user_form})
