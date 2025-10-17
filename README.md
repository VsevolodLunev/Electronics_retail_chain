Electronics Retail Chain

Веб-приложение для управления розничной сетью по продаже электроники с API-интерфейсом и админ-панелью.

Технический стек:

Python 3.8+

Django 5.2.7+ - веб-фреймворк

Django REST Framework 3.16.1+ - API

PostgreSQL - база данных

Poetry - управление зависимостями

DRF Spectacular - Swagger документация

Pytest - тестирование

python-dotenv - управления секретами


Функциональность:

Модели данных:

NetworkNode - узлы сети (заводы, розничные сети, индивидуальные предприниматели)

Product - продукты, связанные с узлами сети


Особенности:

Иерархическая структура сети (3 уровня)

Автоматический расчет уровня иерархии

Задолженность перед поставщиком

Фильтрация по стране и городу

API с ограничениями доступа

Админ-панель с кастомными действиями.


Установка и запуск:

1. Клонирование репозитория


    git clone https://github.com/VsevolodLunev/Electronics_retail_chain.git
    cd Electronics_retail_chain

2. Установка Poetry (если не установлен)


    curl -sSL https://install.python-poetry.org | python3 -

3. Установка зависимостей


    poetry install --only main --with dev --no-root

4. Активация виртуального окружения


    source .venv/bin/activate

5. Настройка базы данных

Создайте базу данных PostgreSQL:

    sql
    CREATE DATABASE electronics_retail_chain;

6. Настройка переменных окружения

Создайте файл .env на основе .env.example:

    cp .env.sample .env
 
Заполните .env файл

7. Применение миграций


    python manage.py makemigrations
    python manage.py migrate

8. Создание суперпользователя


    python manage.py createsuperuser

9. Запуск сервера


    python manage.py runserver

Приложение будет доступно по адресу: 
http://localhost:8000

## API Документация

### Swagger UI
Интерактивная документация API доступна по адресу:  
http://localhost:8000/api/docs/

### ReDoc
Альтернативная документация доступна по адресу:  
http://localhost:8000/api/redoc/

### OpenAPI Schema
Сырая OpenAPI схема доступна по адресу:
http://localhost:8000/api/schema/

## Использование API

### Аутентификация
API требует аутентификации. Доступные методы:
- Сессионная аутентификация (через браузер)
- Basic аутентификация

### Пример запроса с cURL
    '''bash
# Получение списка узлов с Basic аутентификацией
    curl -u username:password http://localhost:8000/api/network-nodes/

# Фильтрация по стране
    curl -u username:password "http://localhost:8000/api/network-nodes/?country=Россия"

# Создание нового узла
    curl -X POST -u username:password \
      -H "Content-Type: application/json" \
      -d '{
      "name": "Новый завод",
      "node_type": "factory",
      "email": "factory@example.com",
      "country": "Россия",
      "city": "Москва",
      "street": "Ленина",
      "house_number": "1"
    }' \
    http://localhost:8000/api/network-nodes/

API Endpoints

Основные endpoints:

GET /api/network-nodes/ - список всех узлов сети
POST /api/network-nodes/ - создание нового узла
GET /api/network-nodes/{id}/ - получение узла по ID
PUT /api/network-nodes/{id}/ - обновление узла
DELETE /api/network-nodes/{id}/ - удаление узла

Дополнительные actions:

POST /api/network-nodes/{id}/clear_debt/ - очистка задолженности
GET /api/network-nodes/{id}/dependent_nodes/ - получение зависимых узлов

Фильтрация:

По стране: ?country=Россия
По городу: ?city=Москва
По типу узла: ?node_type=factory

Админ-панель доступна по адресу: 
http://localhost:8000/admin/

Возможности админ-панели:

Просмотр всех узлов сети и продуктов

Фильтрация по типу узла, стране, городу

Ссылки на поставщиков

Отображение уровня иерархии

Action для очистки задолженности

Inline-редактирование продуктов


Модели данных:


NetworkNode (Звено сети):

-name - Название

-node_type - Тип (factory, retail, entrepreneur)

-email - Email

-country - Страна

-city - Город

-street - Улица

-house_number - Номер дома

-supplier - Поставщик (ссылка на другой NetworkNode)

-debt - Задолженность перед поставщиком

-created_at - Время создания

-hierarchy_level - Уровень иерархии (вычисляемое поле)

-dependent_nodes - Зависимые узлы (обратная связь)


Product (Продукт):

-name - Название продукта

-model - Модель

-release_date - Дата выхода на рынок

-network_node - Связь с узлом сети


Тестирование:

Запуск тестов

# Тесты Pytest
    pytest

# С покрытием кода
    pytest --cov=networknode

# Конкретный тест
    pytest networknode/tests.py::NetworkNodeModelTest

# Через Django test runner
    python manage.py test

Типы тестов

-Модели (создание, валидация, отношения)

-API endpoints (CRUD операции)

-Фильтрация

-Аутентификация и права доступа

# Покрытие тестами: 66%

Разработка:

# Форматирование кода
    black .

# Проверка стиля
    flake8

# Сортировка импортов
    isort .

Продакшен:

Настройки для продакшена:

-Установите DEBUG=False в .env

-Измените SECRET_KEY на надежный

-Используйте PostgreSQL в продакшн-среде

-Настройте статические файлы через Whitenoise


Безопасность:

-API доступен только аутентифицированным пользователям

-Запрещено обновление поля debt через API

-В продакшне включены security middleware

Миграции:

-Создание миграций

    python manage.py makemigrations

-Применение миграций

    python manage.py migrate

-Просмотр SQL миграций

    python manage.py sqlmigrate networknode 0001

Команды управления:

-Создание суперпользователя

    python manage.py createsuperuser

-Запуск shell

    python manage.py shell

-Проверка настроек

    python manage.py check

-Сбор статических файлов

    python manage.py collectstatic

-Dev-сервер с отладкой

# Запуск с Django Debug Toolbar

    python manage.py runserver

# Доступно по http://localhost:8000


Особенности реализации

Автоматическая документация через DRF Spectacular

Защита бизнес-логики - запрет обновления debt через API

Гибкая фильтрация по любым полям

Оптимизированные запросы с select_related и prefetch_related
