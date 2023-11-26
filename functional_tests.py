from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By


class BasicInstallTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_home_page_title(self):
        self.browser.get("http://127.0.0.1:8000")
        # В заголовке сайта - Сайт Арины Крикуновой
        self.assertIn("Сайт Арины Крикуновой", self.browser.title)

    def test_home_header_title(self):
        self.browser.get("http://127.0.0.1:8000")
        header = self.browser.find_element(By.TAG_NAME, "h1")
        # В шапке сайта - Арина Крикунова
        self.assertIn("Арина Крикунова", header.text)

    def test_home_page_blog(self):
        self.browser.get("http://127.0.0.1:8000")
        # Под шапкой расположен блог со статьями
        article_list = self.browser.find_element(By.CLASS_NAME, "article_list")
        self.assertTrue(article_list)

    def test_home_page_articles_look_correct(self):
        self.browser.get("http://127.0.0.1:8000")
        # У каждой статьи есть заголовок и один абзац с текстом
        article_title = self.browser.find_element(By.CLASS_NAME, "article_title")
        article_summary = self.browser.find_element(By.CLASS_NAME, "article_summary")
        self.assertTrue(article_title)
        self.assertTrue(article_summary)


if __name__ == "__main__":
    unittest.main()
