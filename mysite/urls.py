from django.contrib import admin
from django.urls import path
from blog import views

from django.conf import settings
from django.conf.urls.static import static
from blog.views import home_page, article_page, category_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home_page, name="home_page"),
    path("blog/<slug:slug>", views.article_page, name="article_page"),
    path("blog/category/<str:category>/", views.category_page, name="category_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
