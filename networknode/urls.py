from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NetworkNodeViewSet

# Создание router для автоматической генерации URL patterns
router = DefaultRouter()

"""
Регистрация ViewSet в router.

Создает следующие URL patterns:
- GET/POST /api/network-nodes/
- GET/PUT/PATCH/DELETE /api/network-nodes/{id}/
- POST /api/network-nodes/{id}/clear_debt/
"""
router.register(r"network-nodes", NetworkNodeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
