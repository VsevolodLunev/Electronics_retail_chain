#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.insert(0, project_path)


def main():
    """
    Основная функция для выполнения административных задач Django.
    Загружает переменные окружения и выполняет команды Django.
    Raises:
        ImportError: Если Django не установлен или не доступен в PYTHONPATH
    """
    # Загрузка переменных окружения перед настройкой Django
    from dotenv import load_dotenv

    load_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
