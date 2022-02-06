from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..models import Post, Group

User = get_user_model()


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД
        cls.author = User.objects.create_user(username="noname")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_group",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            text="Тестовый заголовок",
            author=cls.author,
            group=cls.group,
        )
        cls.form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            reverse("posts:index"): "posts/index.html",
            reverse(
                "posts:group_list", kwargs={"slug": "test_group"}
            ): "posts/group_list.html",
            reverse(
                "posts:profile", kwargs={"username": "noname"}
            ): "posts/profile.html",
            reverse(
                "posts:post_detail", kwargs={"post_id": "1"}
            ): "posts/post_detail.html",
            reverse("posts:post_create"): "posts/create_post.html",
            reverse(
                "posts:post_edit", kwargs={"post_id": "1"}
            ): "posts/create_post.html",
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def correct_context(self, address):
        """Функция для проверки контекста."""
        response = self.authorized_client.get(address)
        first_object = response.context["page_obj"][0]
        self.assertEqual(first_object.text, "Тестовый заголовок")
        self.assertEqual(first_object.group.title, "Тестовая группа")
        self.assertEqual(first_object.author.username, "noname")

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        self.correct_context(reverse("posts:index"))

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("posts:group_list", kwargs={"slug": "test_group"})
        )
        self.assertEqual(
            response.context["group"].description, "Тестовое описание"
        )
        self.assertEqual(response.context["group"].slug, "test_group")
        self.correct_context(
            reverse("posts:group_list", kwargs={"slug": "test_group"})
        )

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("posts:profile", kwargs={"username": "noname"})
        )
        self.assertEqual(response.context["count_user_posts"], 1)
        self.correct_context(
            reverse("posts:profile", kwargs={"username": "noname"})
        )

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("posts:post_detail", kwargs={"post_id": "1"})
        )
        posts = response.context["post"]
        self.assertEqual(posts.id, self.post.id)
        self.assertEqual(posts.text, "Тестовый заголовок")

    def test_post_create_and_post_edit_show_correct_context(self):
        """Шаблоны post_create, post_edit
        сформированы с правильным контекстом."""
        urls_pages = [
            reverse("posts:post_create"),
            reverse("posts:post_edit", kwargs={"post_id": "1"}),
        ]
        for url in urls_pages:
            response = self.authorized_client.get(url)
            for value, expected in self.form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context.get("form").fields.get(value)
                    self.assertIsInstance(form_field, expected)

    def test_create_new_post(self):
        """Проверка нового поста на главной странице,
        на странице выбранной группы и в профайле пользователя."""

        post = Post.objects.create(
            author=self.author, text=self.post.text, group=self.group
        )
        testing_pages = [
            reverse("posts:index"),
            reverse("posts:group_list", kwargs={"slug": "test_group"}),
            reverse("posts:profile", kwargs={"username": "noname"}),
        ]
        for page in testing_pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertIn(post, response.context["page_obj"])

    def test_post_new_not_in_group(self):
        """Проверка поста в другой группе."""

        response = self.authorized_client.get(reverse("posts:index"))
        post = response.context["page_obj"][0]
        group = post.group
        self.assertEqual(group, self.group)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username="noname")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_group",
            description="Тестовое описание",
        )
        for i in range(13):
            cls.post = Post.objects.create(
                text="Тестовый заголовок", group=cls.group, author=cls.author
            )

        cls.templates = [
            reverse("posts:index"),
            reverse("posts:group_list", kwargs={"slug": "test_group"}),
            reverse("posts:profile", kwargs={"username": "noname"}),
        ]

    def test_first_page_contains_ten_records(self):
        """Paginator предоставляет ожидаемое количество постов
        на первую страницую."""
        for template in self.templates:
            with self.subTest(template=template):
                response = self.client.get(template)
                self.assertEqual(len(response.context["page_obj"]), 10)

    def test_second_page_contains_three_records(self):
        """Paginator предоставляет ожидаемое количество постов
        на вторую страницую."""
        for template in self.templates:
            with self.subTest(template=template):
                response = self.client.get((template) + "?page=2")
                self.assertEqual(len(response.context["page_obj"]), 3)
