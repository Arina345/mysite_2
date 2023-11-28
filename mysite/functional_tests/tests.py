from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from blog.models import Article
from datetime import datetime
import pytz


class BasicInstallTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        Article.objects.create(
            title="title 1",
            summary="summary 1",
            full_text="full_text 1",
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug="a-b-g",
        )

    def tearDown(self):
        self.browser.quit()

    def test_home_page_title(self):
        self.browser.get(self.live_server_url)
        # В заголовке сайта - Сайт Арины Крикуновой
        self.assertIn("Сайт Арины Крикуновой", self.browser.title)

    def test_home_header_title(self):
        self.browser.get(self.live_server_url)
        header = self.browser.find_element(By.TAG_NAME, "h1")
        # В шапке сайта - Арина Крикунова
        self.assertIn("Арина Крикунова", header.text)

    def test_layout_and_styling(self):
        # открываем главную страницу
        self.browser.get(self.live_server_url)
        # устаналвиваем размер окна
        self.browser.set_window_size(1024, 768)
        #
        header = self.browser.find_element(By.TAG_NAME, "h1")

        self.assertTrue(header.location["x"] > 10)

    def test_home_page_blog(self):
        self.browser.get(self.live_server_url)
        # Под шапкой расположен блог со статьями
        article_list = self.browser.find_element(By.CLASS_NAME, "article_list")
        self.assertTrue(article_list)

    def test_home_page_articles_look_correct(self):
        self.browser.get(self.live_server_url)
        # У каждой статьи есть заголовок и один абзац с текстом
        article_title = self.browser.find_element(By.CLASS_NAME, "article_title")
        article_summary = self.browser.find_element(By.CLASS_NAME, "article_summary")
        self.assertTrue(article_title)
        self.assertTrue(article_summary)

    def test_home_page_article_title_link_leads_to_article_page(self):
        # кликнув по заголовку открывается полный текст статьи
        # открываем главную страницу
        self.browser.get(self.live_server_url)
        # находим статью
        article_title = self.browser.find_element(By.CLASS_NAME, "article_title")
        article_title_text = article_title.text

        # находим ссылку в заголовке статьи
        article_link = article_title.find_element(By.TAG_NAME, "a")
        # переходим по ссылке
        self.browser.get(article_link.get_attribute("href"))
        article_page_title = self.browser.find_element(By.CLASS_NAME, "article_title")

        # ожидаем,что на открывашиеся странице есть нужная статья
        self.assertEqual(article_title_text, article_page_title.text)


# при открытии несущ. стр. открылась страничка "Страница не найдена"
