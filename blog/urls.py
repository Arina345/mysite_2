from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "blog"

urlpatterns = [
    # представление статьи. Это то,что мы видим в первую очередь когда перейдем по адресу blog/,а именно все статьи
    path("", views.article_list, name="article_list"),
    # Для захвата значений из URL-адреса используются угловые скобки.
    path("<slug:article>/", views.article_detail, name="article_detail"),
    path("mine/", views.ManageArticleListView.as_view(), name="manage_article_list"),
    path("create/", views.ArticleCreateView.as_view(), name="article_create"),
    path("<pk>/edit/", views.ArticleUpdateView.as_view(), name="article_edit"),
    path("<pk>/delete/", views.ArticleDeleteView.as_view(), name="article_delete"),
]
