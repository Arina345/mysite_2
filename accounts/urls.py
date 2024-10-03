from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("", views.dashboard, name="dashboard"),
    path("dashboard/<str:username>/", views.dashboard, name="dashboard_username"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
]
