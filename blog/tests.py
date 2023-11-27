from django.test import TestCase
from django.urls import resolve
from blog.views import home_page
from django.http import HttpRequest
from blog.models import Article
from datetime import datetime


class ArticlePageTest(TestCase):
    def test_article_displays_correct_article(self):
        Article.objects.create(
            title="title 1",
            summary="summary 1",
            full_text="full_text 1",
            pubdate=datetime.now(),
        )

        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf8")

        self.assertIn("title 1", html)
        self.assertIn("full_text 1", html)
        self.assertNotIn("summary 1", html)


class HomePageTest(TestCase):
    def test_home_page_displays_articles(self):
        Article.objects.create(
            title="title 1",
            summary="summary 1",
            full_text="full_text 1",
            pubdate=datetime.now(),
        )
        Article.objects.create(
            title="title 2",
            summary="summary 2",
            full_text="full_text 2",
            pubdate=datetime.now(),
        )

        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title> Сайт Арины Крикуновой </title>", html)
        self.assertIn("<h1> Арина Крикунова </h1", html)
        self.assertTrue(html.endswith("</html>"))

    def test_root_url_resolves_to_home_page_views(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        html = response.content.decode("utf8")

        self.assertIn("title 1", html)
        self.assertIn("blog/title-1", html)
        self.assertIn("summary 1", html)
        self.assertNotIn("full_text 1", html)

        self.assertIn("title 2", html)
        self.assertIn("blog/title-2", html)
        self.assertIn("summary 2", html)
        self.assertNotIn("full_text 2", html)


class ArticleModelTest(TestCase):
    def test_article_model_save_and_retieve(self):
        # создай статью 1
        # сохрани статью 1  в базе
        article1 = Article(
            title="article 1",
            full_text="full_text 1",
            summary="summary 1",
            category="category 1",
            pubdate=datetime.now(),
        )
        article1.save()
        # создай статью 2
        # сохрани статью 2  в базе
        article2 = Article(
            title="article 2",
            full_text="full_text 2",
            summary="summary 2",
            category="category 2",
            pubdate=datetime.now(),
        )
        article2.save()
        # загрузи из базы все стаьи
        all_articles = Article.objects.all()
        # проверь:статей должно быть 2

        self.assertEqual(len(all_articles), 2)

        # проверь:1 загруженная статья из базы == статья 1
        self.assertEqual(all_articles[0].title, article1.title)

        # проверь:2 загруженная статья из базы == статья 2
        self.assertEqual(all_articles[1].title, article2.title)


# Некоторые статьи есть в админке,но они не опубликованы
# Статьи открываются с красивым и коротким адресом
