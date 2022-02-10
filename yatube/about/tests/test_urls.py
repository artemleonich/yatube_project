from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls_exists(self):
        """Страницы доступны любому пользователю."""
        urls_statuses = {
            "/": HTTPStatus.OK,
            "/about/author/": HTTPStatus.OK,
            "/about/tech/": HTTPStatus.OK,
        }
        for urls, status in urls_statuses.items():
            with self.subTest(urls=urls):
                response = self.guest_client.get(urls)
                self.assertEqual(response.status_code, status)
