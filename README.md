# Yatube

**[Русский](#русский) | [English](#english)**

---

## Русский

### Описание

Yatube — социальная блог-платформа, созданная на Django. Позволяет пользователям публиковать посты с изображениями, объединять их в тематические группы, подписываться на авторов и оставлять комментарии.

### Возможности

- Регистрация и аутентификация пользователей
- Создание, редактирование и удаление постов
- Прикрепление изображений к постам
- Группировка постов по тематическим сообществам
- Комментарии к публикациям
- Система подписок на авторов
- Лента постов от избранных авторов
- Пагинация
- Кэширование страниц

### Технологии

- Python 3.10
- Django 2.2.19
- SQLite
- Unittest
- django-debug-toolbar 3.2.4

### Структура проекта

```
yatube_project/
├── yatube/
│   ├── about/          # Приложение статических страниц
│   ├── core/           # Общие утилиты и контекст-процессоры
│   ├── posts/          # Основное приложение (посты, группы, комментарии, подписки)
│   │   ├── tests/      # Тесты моделей, представлений, форм и URL
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   ├── users/          # Приложение пользователей
│   ├── static/         # Статические файлы (CSS, JS, изображения)
│   ├── templates/      # HTML-шаблоны
│   └── yatube/         # Настройки проекта
├── requirements.txt
└── README.md
```

### Запуск проекта

Клонируйте репозиторий:

```bash
git clone https://github.com/artemleonich/yatube_project.git
cd yatube_project
```

Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Выполните миграции:

```bash
cd yatube
python3 manage.py migrate
```

Запустите сервер разработки:

```bash
python3 manage.py runserver
```

Проект будет доступен по адресу http://127.0.0.1:8000/

### Запуск тестов

```bash
cd yatube
python3 manage.py test
```

### Автор

Артём — [GitHub](https://github.com/artemleonich)

### Лицензия

Проект распространяется под лицензией [MIT](LICENSE).

---

## English

### Description

Yatube is a social blogging platform built with Django. It allows users to publish posts with images, organize them into thematic groups, follow authors, and leave comments.

### Features

- User registration and authentication
- Create, edit, and delete posts
- Attach images to posts
- Group posts by thematic communities
- Comment on publications
- Author subscription system
- Feed of posts from followed authors
- Pagination
- Page caching

### Tech Stack

- Python 3.10
- Django 2.2.19
- SQLite
- Unittest
- django-debug-toolbar 3.2.4

### Project Structure

```
yatube_project/
├── yatube/
│   ├── about/          # Static pages app
│   ├── core/           # Shared utilities and context processors
│   ├── posts/          # Main app (posts, groups, comments, follows)
│   │   ├── tests/      # Tests for models, views, forms, and URLs
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   ├── users/          # Users app
│   ├── static/         # Static files (CSS, JS, images)
│   ├── templates/      # HTML templates
│   └── yatube/         # Project settings
├── requirements.txt
└── README.md
```

### Getting Started

Clone the repository:

```bash
git clone https://github.com/artemleonich/yatube_project.git
cd yatube_project
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
cd yatube
python3 manage.py migrate
```

Start the development server:

```bash
python3 manage.py runserver
```

The project will be available at http://127.0.0.1:8000/

### Running Tests

```bash
cd yatube
python3 manage.py test
```

### Author

Artem — [GitHub](https://github.com/artemleonich)

### License

This project is licensed under the [MIT](LICENSE) License.
