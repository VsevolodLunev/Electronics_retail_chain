import django
import pytest


def test_django_is_configured():
    """Базовый тест для проверки что Django настроен."""
    assert django.conf.settings.configured
    assert django.conf.settings.SECRET_KEY is not None


@pytest.mark.django_db
def test_database_access():
    """Тест для проверки доступа к базе данных."""
    from django.contrib.auth.models import User

    user_count = User.objects.count()
    assert user_count >= 0
