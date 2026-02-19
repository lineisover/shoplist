# ShopList

Веб-приложение для создания и управления списками покупок с возможностью совместной работы.

Проект реализован на Django с использованием HTMX для частичного обновления интерфейса без перезагрузки страницы.

## Функциональность

- Регистрация и авторизация пользователей
- Создание пространств (spaces)
- Добавление пользователей в пространство
- Создание списков покупок
- Добавление и удаление элементов
- Отметка элементов как выполненных
- Динамическое обновление интерфейса через HTMX

## Технологии

- Python 3.12+
- Django
- HTMX
- SQLite (по умолчанию)
- Gunicorn (production)

## Установка и запуск

### Клонирование репозитория

```bash
git clone https://github.com/your_username/shoplist.git
cd shoplist
```

### Создание виртуального окружения

```bash
python -m venv .venv
```

Активация:

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Настройка переменных окружения

Создать файл `.env`:

```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///db.sqlite3
```

### Применение миграций

```bash
python manage.py migrate
```

### Создание суперпользователя

```bash
python manage.py createsuperuser
```

### Запуск сервера

```bash
python manage.py runserver
```

Приложение будет доступно по адресу:

```
http://127.0.0.1:8000
```

## Структура проекта

```
config/          # настройки Django
shoplist/        # основное приложение
templates/       # HTML-шаблоны
manage.py
```

## Production запуск

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Лицензия

MIT
