# Yatube

Социальная сеть для публикации дневников. Позволяет создавать посты с текстом и изображениями, подписываться на авторов, оставлять комментарии и объединять записи в тематические группы.

### Технологии

- Python 3.10
- Django 2.2.19

### Запуск проекта в dev-режиме

Клонировать репозиторий и перейти в него:

```bash
git clone git@github.com:artemleonich/yatube_project.git
cd yatube_project
```

Создать и активировать виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
cd yatube
python3 manage.py migrate
```

Запустить сервер:

```bash
python3 manage.py runserver
```

### Автор

Артём
