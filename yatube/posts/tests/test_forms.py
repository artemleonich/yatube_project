from django.contrib.auth import get_user_model
from http import HTTPStatus
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, Comment

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
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        uploaded = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )
        form_data = {
            "text": "Текст поста",
            "group": self.group.id,
            "image": uploaded,
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
        self.assertEqual(latest_post.text, form_data["text"])
        self.assertEqual(latest_post.group.id, self.group.id)
        self.assertEqual(latest_post.author, self.user)
        self.assertTrue(
            Post.objects.filter(image=Post.objects.first().image).exists()
        )

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
        self.assertEqual(latest_post.text, form_data["text"])
        self.assertEqual(latest_post.group.id, self.group.id)
        self.assertEqual(latest_post.author, self.user)

    def test_non_authorize_client_comment(self):
        """Комментировать пост может только авторизованный пользователь."""
        comments_count = Comment.objects.count()
        form_data = {"text": "Тестовый текст комментария"}
        response = self.guest_client.post(
            reverse("posts:add_comment", kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("users:login")
            + "?next="
            + reverse(
                "posts:add_comment",
                kwargs={"post_id": self.post.id},
            ),
        )
        self.assertEqual(Comment.objects.count(), comments_count)

    def test_succesful_comment_appear_in_page(self):
        """После успешной отправки комментарий появляется на странице поста."""
        comments_count = Comment.objects.count()
        form_data = {
            "text": "Тестовый текст комментария",
            "author": self.post.author.username,
        }
        self.authorized_client.post(
            reverse("posts:add_comment", kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True,
        )
        self.authorized_client.get(
            reverse("posts:post_detail", kwargs={"post_id": self.post.id}),
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        latest_comment = Comment.objects.get(id=self.post.id)
        self.assertEqual(latest_comment.text, form_data["text"])
        self.assertEqual(latest_comment.author.username, form_data["author"])
