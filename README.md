# Yatube

<a href=".github/assets/light/stack.svg#gh-light-mode-only"><img src=".github/assets/light/stack.svg" height="28" alt="Python · Django · Learning" /></a><a href=".github/assets/stack.svg#gh-dark-mode-only"><img src=".github/assets/stack.svg" height="28" alt="Python · Django · Learning" /></a>

Публикации, комментарии и лента любимых авторов.

**Учебный проект**  
[Русский](#about) · [English](#english) · [Профиль](https://github.com/artemleonich)

<a id="about"></a>

## О проекте

Учебная блог-платформа на Django: публикации, тематические группы, комментарии и подписки на авторов. В репозитории собрана версия Yatube с тестами приложения и настройками Django Debug Toolbar.

- Регистрация, вход и профили авторов.
- Создание текстовых постов и редактирование собственных публикаций.
- Тематические группы и пагинация лент.
- Изображения в публикациях, комментарии и страницы отдельных записей.
- Подписка и отписка от авторов, отдельная лента подписок.
- Кеширование блока главной ленты на 20 секунд.
- Страницы ошибок и админ-панель Django.

Учебные этапы проекта: [сообщества](https://github.com/artemleonich/hw02_community) · [формы](https://github.com/artemleonich/hw03_forms) · [тесты](https://github.com/artemleonich/hw04_tests) · [финальный этап](https://github.com/artemleonich/hw05_final).

## Запуск

```bash
git clone https://github.com/artemleonich/yatube_project.git
cd yatube_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Dependencies used by the project but missing from requirements.txt
python -m pip install Pillow==8.3.1 sorl-thumbnail==12.7.0
python yatube/manage.py migrate
python yatube/manage.py createsuperuser
python yatube/manage.py runserver
```

В Windows PowerShell: `.venv\Scripts\Activate.ps1`.

Приложение доступно по адресу [127.0.0.1:8000](http://127.0.0.1:8000/). Суперпользователь нужен для [админ-панели](http://127.0.0.1:8000/admin/), где можно создать тематические группы.

В [requirements.txt](requirements.txt) отсутствуют `Pillow` и `sorl-thumbnail`, хотя они используются приложением. Отдельная команда выше добавляет версии из учебного [hw05_final](https://github.com/artemleonich/hw05_final/blob/master/requirements.txt); файл зависимостей в этом репозитории сохранён в исходном виде.

## Проверка

Тесты приложения запускаются из корня репозитория через Django:

```bash
python yatube/manage.py test posts about core
```

В `yatube/posts/tests/` находятся проверки моделей, маршрутов, представлений и форм.

## Навигация по коду

| Путь | Назначение |
| --- | --- |
| [yatube/posts/](yatube/posts/) | Посты, комментарии, подписки и формы |
| [yatube/users/](yatube/users/) | Регистрация и авторизация |
| [yatube/core/](yatube/core/) | Страницы ошибок и общие функции |
| [yatube/templates/](yatube/templates/) | HTML-шаблоны |
| [yatube/posts/tests/](yatube/posts/tests/) | Тесты приложения |
| [yatube/yatube/settings.py](yatube/yatube/settings.py) | SQLite, медиафайлы и кеш |

## Статус

Сохранён учебный стек Django 2.2. Запуск на новых версиях Python может потребовать адаптации окружения. В текущей реализации картинку можно загрузить при редактировании поста; форма создания не обрабатывает файлы.

<a id="english"></a>

<details>
<summary>English overview</summary>

A Django learning project with posts, groups, images, comments, author follows and a following feed. Application tests use Django TestCase. The requirements file is missing Pillow and sorl-thumbnail; install the supplemental versions shown above to reproduce the image-related dependencies from the final learning stage.

Create a virtual environment, install the dependencies, run `python yatube/manage.py migrate`, optionally create an admin account, then start `python yatube/manage.py runserver`. Run `python yatube/manage.py test posts about core` for Django tests.

The code retains the original Django 2.2 learning stack. Image uploads are handled when editing a post; the creation view does not process uploaded files. The main feed fragment is cached for twenty seconds.

</details>

---

Автор: [Артём Леонов](https://github.com/artemleonich).

Лицензия: [MIT](LICENSE).

