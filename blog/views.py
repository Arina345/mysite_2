from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article

# UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required


# from .models import Profile
from django.contrib import messages
from django.views.generic.list import ListView


# В данном представлении извлекаются все посты со статусом PUBLISHED,
# используя менеджер published, который мы создали ранее.


def article_list(request):
    articles = Article.published.all()
    # render - сокращенный доступ
    # request, путь к шаблону,для прорисовки отображения статей
    return render(request, "blog/article/list.html", {"articles": articles})


# Это представление детальной информации о посте.s
# Было
# def article_detail(request, id):
#     try:
#         # извдечение статьи с указанным id
#         article = Article.published.get(id=id)
#     except Article.DoesNotExist:
#         raise Http404("Страница не найдена")

#     return render(render, "blog/article/detail.html", {"article": article})


# Улучшено
# Использована функция сокращенного доступа get_object_or_404
def article_detail(request, article):
    article = get_object_or_404(Article, slug=article, status=Article.Status.PUBLISHED)
    return render(request, "blog/article/detail.html", {"article": article})


# ---------------------------------------------------------------------------------------------------------------
# Оно наследует от встроенного в  Django типового представления ListView.
# Здесь переопределяется метод
# get_queryset() представления, чтобы извлекать только те курсы, которые были
# созданы текущим пользователем. Для того чтобы запретить пользователям
# редактировать, обновлять или удалять курсы, которые они не создавали,
# также потребуется переопределить метод get_queryset() в  представлениях
# создания, обновления и удаления.


class ManageArticleListView(ListView):
    model = Article
    # отображение списка статей
    # template_name = "blog/manage/article/list.html"
    template_name = "accounts/dashbosrd.html"

    def get_queryset(self):
        qs = super().get_queryset()
        # только те статьи,которые принадлежат пользователю
        return qs.filter(author=self.request.user)


# CreateView - это представление, которое отображает форму для создания нового экземпляра модели.
# Оно использует шаблон для отображения формы и обрабатывает проверку и создание нового экземпляра.

# UpdateView - это представление, которое отображает форму для обновления существующего экземпляра модели.
# Оно использует шаблон для отображения формы и обрабатывает проверку и обновление существующего экземпляра.

# DeleteView - это представление, которое удаляет существующий экземпляр модели.
# Обычно оно использует шаблон для подтверждения удаления и обрабатывает удаление экземпляра.


# Эти примеси будут использоваться вместе со встроенными в Django представлениями ListView, CreateView, UpdateView и DeleteView.
class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.author = self.request.user
        # Метод form_valid() исполняется, когда переданная на обработку форма является валидной.
        return super().form_valid(form)


class OwnerArticleMixin(OwnerMixin):
    model = Article
    fields = ["title", "slug", "summary", "status", "full_text"]
    # Здесь указывается URL-адрес, на который пользователь
    # должен быть перенаправлен после успешного создания или редактирования Article объекта.
    success_url = reverse_lazy("blog:article_list")


# template_name: шаблон, который будет использоваться для представлений CreateView и UpdateView.
class OwnerArticleEditMixin(OwnerArticleMixin, OwnerEditMixin):
    template_name = "blog/manage/article/form.html"


# Этот код определяет класс представления Django,
# ManageArticleListView который наследуется от обоих OwnerArticleMixin и ListView.


# выводит список созданных пользователем статей.
# Указанное представление наследует от OwnerArticleMixin и ListView
# и определяет специальный атрибут template_name для шаблона, который
# будет выводить список статей;
class ManageArticleListView(OwnerArticleMixin, ListView):
    template_name = template_name = "accounts/dashbosrd.html"
    # permission_required = "blog.view_article"


# Создание статьи
class ArticleCreateView(OwnerArticleEditMixin, CreateView):
    permission_required = "blog.add_article"
    # pass


# Редактирование статьи
class ArticleUpdateView(OwnerArticleEditMixin, UpdateView):
    permission_required = "blog.change_article"
    # pass


# Удаление статьи
class ArticleDeleteView(OwnerArticleMixin, DeleteView):
    template_name = "blog/manage/article/delete.html"
    permission_required = "blog.delete_article"
