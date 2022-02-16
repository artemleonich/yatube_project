from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

from ..models import Post, Group, Follow

User = get_user_model()

POST_COUNT = 1
POSTS_LIMIT = 10


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title="Тестовый заголовок",
            description="Тестовое описание",
            slug="test_group",
        )
        cls.user = User.objects.create_user(username="noname")
        cls.post = Post.objects.create(
            author=cls.user,
            text="Текст поста",
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse("posts:index"): "posts/index.html",
            reverse(
                "posts:group_list",
                kwargs={"slug": self.group.slug},
            ): "posts/group_list.html",
            reverse(
                "posts:profile",
                kwargs={"username": self.user},
            ): "posts/profile.html",
            reverse(
                "posts:post_detail",
                kwargs={"post_id": self.post.id},
            ): "posts/post_detail.html",
            reverse("posts:post_create"): "posts/create_post.html",
            reverse(
                "posts:post_edit",
                kwargs={"post_id": self.post.id},
            ): "posts/create_post.html",
        }
        for (
            reverse_name,
            template,
        ) in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse("posts:index"))
        post_in_page = response.context["page_obj"][0]
        self.assertEqual(post_in_page.text, self.post.text)
        self.assertEqual(post_in_page.author.username, self.user.username)
        self.assertEqual(post_in_page.group.title, self.group.title)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse(
                "posts:group_list",
                kwargs={"slug": self.group.slug},
            )
        )
        post_in_page = response.context["page_obj"][0]
        self.assertEqual(post_in_page.group.title, self.group.title)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse(
                "posts:profile",
                kwargs={"username": self.user},
            )
        )
        post_in_page = response.context["page_obj"][0]
        self.assertEqual(post_in_page.author.username, self.user.username)
        self.assertEqual(len(response.context["page_obj"]), POST_COUNT)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse(
                "posts:post_detail",
                kwargs={"post_id": self.post.id},
            )
        )
        post_in_page = response.context["post"]
        self.assertEqual(post_in_page.id, self.post.id)
        self.assertEqual(post_in_page.author.username, self.user.username)

    def test_post_create_and_post_edit_show_correct_context(
        self,
    ):
        """Шаблоны post_create, post_edit
        сформированы с правильным контекстом."""
        response1 = self.authorized_client.get(reverse("posts:post_create"))
        response2 = self.authorized_client.get(
            reverse(
                "posts:post_edit",
                kwargs={"post_id": self.post.id},
            )
        )
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field1 = response1.context.get("form").fields.get(value)
                form_field2 = response2.context.get("form").fields.get(value)
                self.assertIsInstance(form_field1, expected)
                self.assertIsInstance(form_field2, expected)

    def test_images_appears_in_pages(self):
        """При выводе поста с картинкой
        изображение появлется на нужных страницах."""
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
        self.post_with_picture = Post.objects.create(
            author=self.user,
            text="Новый текст с картинкой",
            group=self.group,
            image=uploaded,
        )
        urls = (
            reverse("posts:index"),
            reverse("posts:profile", kwargs={"username": self.user}),
            reverse("posts:group_list", kwargs={"slug": self.group.slug}),
            reverse("posts:post_detail", kwargs={"post_id": self.post.id}),
        )
        for url in urls:
            with self.subTest(url=url):
                self.guest_client.get(url)
                self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_cache_index(self):
        """Проверка работы кэширования."""
        cache1 = self.authorized_client.get(reverse("posts:index")).content
        form_data = {
            "group": self.group,
            "text": "кэш",
        }
        self.authorized_client.post(
            reverse("posts:post_create"), data=form_data, follow=True
        )
        cache2 = self.authorized_client.get(reverse("posts:index")).content
        self.assertEqual(cache2, cache1)
        cache.clear()
        response_cache = self.authorized_client.get(
            reverse("posts:index")
        ).content
        self.assertNotEqual(response_cache, cache1)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title="Тестовый заголовок",
            description="Тестовое описание",
            slug="test_group",
        )
        cls.user = User.objects.create_user(username="noname")
        cls.posts_count = 13
        cls.objects = [
            Post(
                author=cls.user,
                text="Текст поста",
                group=cls.group,
            )
            for _ in range(cls.posts_count)
        ]
        Post.objects.bulk_create(cls.objects, cls.posts_count)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        """Paginator предоставляет ожидаемое количество постов
        на первую страницую."""
        response = self.guest_client.get(reverse("posts:index"))
        self.assertEqual(len(response.context["page_obj"]), POSTS_LIMIT)

    def test_second_page_contains_three_records(self):
        """Paginator предоставляет ожидаемое количество постов
        на вторую страницую."""
        response = self.guest_client.get(reverse("posts:index") + "?page=2")
        self.assertEqual(
            len(response.context["page_obj"]),
            self.posts_count % POSTS_LIMIT,
        )


class FollowTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="TestAuthor")
        self.user = User.objects.create_user(username="TestUser")
        self.authorize_client = Client()
        self.authorize_client.force_login(self.user)

    def test_auth_user_can_follow(self):
        """Авторизованный пользователь может подписываться."""
        follow_count = Follow.objects.count()
        self.authorize_client.get(
            reverse(
                "posts:profile_follow",
                kwargs={"username": self.author.username},
            )
        )
        follow = Follow.objects.first()
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertEqual(follow.author, self.author)
        self.assertEqual(follow.user, self.user)

    def test_auth_user_can_unfollow(self):
        """Авторизованный пользователь может отписываться."""
        follow_count = Follow.objects.count()
        Follow.objects.create(user=self.user, author=self.author)
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.authorize_client.get(
            reverse(
                "posts:profile_unfollow",
                kwargs={"username": self.author.username},
            )
        )
        self.assertEqual(Follow.objects.count(), follow_count)

    def test_new_post_appear_in_follower_page(self):
        """Новая запись автора появляется в ленте тех, кто на него подписан."""
        self.post = Post.objects.create(
            text="Тестовый текст", author=self.author
        )
        Follow.objects.create(author=self.author, user=self.user)
        response = self.authorize_client.get(reverse("posts:follow_index"))
        self.assertEqual(response.context["page_obj"][0], self.post)

    def test_new_post_dont_appear_in_follower_page(self):
        """Новая запись автора не появляется в ленте тех,
        кто на не него подписан."""
        self.post = Post.objects.create(
            text="Тестовый текст", author=self.author
        )
        Follow.objects.create(author=self.author, user=self.user)
        self.second_user = User.objects.create_user(
            username="username",
        )
        self.authorize_client.force_login(self.second_user)
        response = self.authorize_client.get(reverse("posts:follow_index"))
        self.assertEqual(len(response.context["page_obj"]), 0)
