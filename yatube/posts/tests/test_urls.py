from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username="noname")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_group",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            text="Тестовый заголовок",
            author=cls.author,
        )
        cls.id = cls.post.id

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_guest_client = {
            "/": "posts/index.html",
            "/group/test_group/": "posts/group_list.html",
            f"/profile/{self.author}/": "posts/profile.html",
            f"/posts/{self.id}/": "posts/post_detail.html",
            f"/posts/{self.id}/edit/": "posts/create_post.html",
            "/create/": "posts/create_post.html",
        }
        for (
            urls,
            template,
        ) in templates_url_guest_client.items():
            with self.subTest(urls=urls):
                response = self.authorized_client.get(urls)
                self.assertTemplateUsed(response, template)

    def test_urls_for_all(self):
        """Страницы доступны любому пользователю."""
        templates_urls_all = {
            "/": HTTPStatus.OK,
            "/group/test_group/": HTTPStatus.OK,
            f"/profile/{self.author}/": HTTPStatus.OK,
            f"/posts/{self.id}/": HTTPStatus.OK,
            "/unexiscting_page/": HTTPStatus.NOT_FOUND,
        }
        for urls, status in templates_urls_all.items():
            with self.subTest(urls=urls):
                response = self.guest_client.get(urls)
                self.assertEqual(response.status_code, status)

    def test_post_create_url_for_authorized(self):
        """Страница доступна только авторизованному пользователю."""
        response = self.authorized_client.get(reverse("posts:post_create"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_for_author(self):
        """Страница доступна автору поста."""
        response = self.authorized_client.get(
            reverse(
                "posts:post_edit",
                kwargs={"post_id": self.id},
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
