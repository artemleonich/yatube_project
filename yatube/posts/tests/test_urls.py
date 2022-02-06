from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_about_author(self):
        response = self.guest_client.get("/about/author/")
        self.assertEqual(response.status_code, 200)

    def test_about_tech(self):
        response = self.guest_client.get("/about/tech/")
        self.assertEqual(response.status_code, 200)


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

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_guest_client = {
            "/": "posts/index.html",
            "/group/test_group/": "posts/group_list.html",
            "/profile/noname/": "posts/profile.html",
            "/posts/1/": "posts/post_detail.html",
            "/unexisting_page/": "unexisting_page.html",
        }
        for address, template in templates_url_guest_client.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                if address == "/unexisting_page/":
                    self.assertEqual(response.status_code, 404)
                else:
                    self.assertEqual(response.status_code, 200)

        templates_url_authorized_client = {
            "/": "posts/index.html",
            "/group/test_group/": "posts/group_list.html",
            "/profile/noname/": "posts/profile.html",
            "/posts/1/": "posts/post_detail.html",
            "/create/": "posts/create_post.html",
            "/posts/1/edit/": "posts/create_post.html",
        }
        for address, template in templates_url_authorized_client.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                if address == "/unexisting_page/":
                    self.assertEqual(response.status_code, 404)
                else:
                    self.assertEqual(response.status_code, 200)
