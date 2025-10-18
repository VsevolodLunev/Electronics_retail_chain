import os

import django
import pytest
from django.conf import settings


def pytest_configure():
    """
    Конфигурация pytest для Django.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    if not settings.configured:
        # Импортируем настоящие настройки из проекта
        from config import settings as project_settings

        # Используем настройки из проекта, но переопределяем базу данных для тестов
        test_settings = {
            "DATABASES": {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            "INSTALLED_APPS": project_settings.INSTALLED_APPS,
            "SECRET_KEY": project_settings.SECRET_KEY,
            "USE_TZ": project_settings.USE_TZ,
            "ROOT_URLCONF": project_settings.ROOT_URLCONF,
            "MIDDLEWARE": project_settings.MIDDLEWARE,
            "TEMPLATES": project_settings.TEMPLATES,
            "REST_FRAMEWORK": project_settings.REST_FRAMEWORK,
            "LANGUAGE_CODE": project_settings.LANGUAGE_CODE,
            "TIME_ZONE": project_settings.TIME_ZONE,
            "USE_I18N": project_settings.USE_I18N,
            "USE_L10N": project_settings.USE_L10N,
            "DEFAULT_AUTO_FIELD": project_settings.DEFAULT_AUTO_FIELD,
        }

        # Копируем все атрибуты из настоящих настроек
        for attr in dir(project_settings):
            if not attr.startswith("_") and attr not in test_settings:
                test_settings[attr] = getattr(project_settings, attr)

        settings.configure(**test_settings)

    django.setup()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Фикстура для автоматического предоставления доступа к БД всем тестам.
    """
    pass
