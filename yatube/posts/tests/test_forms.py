from django.contrib.auth import get_user_model
from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="noname")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_group",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Текст поста",
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_new_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            "text": "Текст поста",
            "group": self.group.id,
        }
        response = self.authorized_client.post(
            reverse("posts:post_create"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response,
            reverse(
                "posts:profile",
                kwargs={"username": self.user},
            ),
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        latest_post = Post.objects.first()
        self.assertEqual(latest_post.text, form_data.get("text"))
        self.assertEqual(latest_post.group.id, self.group.id)
        self.assertEqual(latest_post.author, self.user)

    def test_edit_post(self):
        """Валидная форма редактирует запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            "text": "Текст поста2",
            "group": self.group.id,
        }
        response = self.authorized_client.post(
            reverse(
                "posts:post_edit",
                kwargs={"post_id": self.post.id},
            ),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response,
            reverse(
                "posts:post_detail",
                kwargs={"post_id": self.post.id},
            ),
        )
        self.assertEqual(Post.objects.count(), posts_count)
        latest_post = Post.objects.get(id=self.post.id)
        self.assertEqual(latest_post.text, form_data.get("text"))
        self.assertEqual(latest_post.group.id, self.group.id)
        self.assertEqual(latest_post.author, self.user)
