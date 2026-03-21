# Правила работы с Qwen Code в проекте Jobify

## 📌 О проекте

**Jobify** — аналитическая платформа для исследования рынка труда на основе данных hh.ru.

- **Фреймворк:** Django 5.x
- **Язык:** Python 3.11+
- **База данных:** PostgreSQL 15
- **Кэш/очереди:** Redis 7
- **Задачи по расписанию:** Celery + Celery Beat
- **HTTP-запросы:** httpx (асинхронные)
- **Визуализация:** Chart.js + Plotly.js
- **CSS/JS:** Bootstrap 5, Alpine.js, HTMX
- **Контейнеры:** Docker + Docker Compose
- **Статическая типизация:** mypy

## 📁 Структура проекта

```
Jobify/
├── core/                   # Настройки Django, Celery
├── parser/                 # Приложение парсинга (модели, сервисы, задачи)
├── analytics/              # Приложение аналитики (views, шаблоны)
├── static/                 # Статические файлы
├── templates/              # Общие шаблоны
├── .env                    # Переменные окружения
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

## 🔑 API hh.ru

Проект использует API hh.ru для получения вакансий:
- `GET /vacancies` — поиск вакансий
- `GET /vacancies/{id}` — детали вакансии
- `GET /areas` — регионы
- `GET /industries` — отрасли
- `GET /currencies` — валюты

**Важно:** Работаем только с публичными данными о вакансиях (не резюме).

## 🤖 Правила взаимодействия с Qwen Code

### 1. Только подсказываю и направляю
Я не выполняю задачи за тебя, а помогаю разобраться:
- Объясняю концепции и подходы
- Предлагаю варианты решения
- Указываю на потенциальные проблемы
- Помогаю с архитектурными решениями

### 2. Никакого готового кода без разрешения
- **Никогда не пишу полный код** без явного запроса
- Если нужен код — пользователь должен прямо попросить: «напиши код», «покажи пример»
- По умолчанию даю объяснения, псевдокод, ссылки на документацию
- Могу показать фрагменты для иллюстрации концепции

### 3. Лучшие практики разработки
- Придерживаемся **PEP 8**, **SOLID**, **DRY**, **KISS**
- Код должен быть **читаемым**, **тестируемым**, **поддерживаемым**
- Предпочитаем простые решения сложным, если нет веских причин
- Всегда думаем о масштабируемости и производительности

## 🛠 Правила разработки

### Код
- Следовать PEP 8
- Использовать type hints для функций
- Добавлять docstring для классов и публичных функций
- Импорты сортировать: stdlib → third-party → local

### Типизация
- Использовать type hints для всех функций
- Запускать mypy для проверки типов
- Для Django моделей использовать `django-stubs`

### Django
- Использовать Class-Based Views где уместно
- Бизнес-логика в сервисах (`services/`), не в views
- Формы и валидация через Django Forms или Pydantic
- Миграции создавать после изменений моделей

### Асинхронность
- HTTP-запросы к API через `httpx` (async)
- Celery задачи для фонового парсинга

### Тесты
- Использовать pytest + pytest-django
- Покрывать критическую логику (парсинг, аналитика)

### Docker
- Запуск через `docker-compose up`
- Переменные окружения в `.env`

## 📝 Конвенции именования

- **Переменные и функции:** `snake_case` — `get_vacancies`, `salary_min`
- **Классы:** `PascalCase` — `Vacancy`, `HhApiClient`
- **Константы:** `UPPER_SNAKE` — `HH_API_URL`, `MAX_RETRIES`
- **Файлы шаблонов:** `snake_case.html` — `vacancy_list.html`
- **Celery задачи:** `snake_case` — `parse_vacancies_task`

## 🔐 Безопасность

- **Никогда не коммитить** `.env` с токенами API
- Токен hh.ru хранить в `HH_API_TOKEN` в `.env`
- Использовать `django-environ` для загрузки переменных

## 🚀 Команды разработки

```bash
# Запуск через Docker
docker-compose up

# Запуск Django (локально)
python manage.py runserver

# Celery worker
celery -A core worker -l info

# Celery Beat (расписание)
celery -A core beat -l info

# Миграции
python manage.py makemigrations
python manage.py migrate

# Тесты
pytest
pytest --cov=parser --cov=analytics

# Проверка типов
mypy parser/ analytics/ core/

# Линтинг (если настроен)
ruff check .
black .
```

## 📚 Полезные ссылки

- Документация API hh.ru: https://api.hh.ru/openapi/redoc
- Портал разработчиков hh.ru: https://dev.hh.ru/
- Django docs: https://docs.djangoproject.com/
- Celery docs: https://docs.celeryq.dev/
- Mypy docs: https://mypy.readthedocs.io/
- Django-stubs: https://github.com/typeddjango/django-stubs
