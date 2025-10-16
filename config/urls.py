from django.contrib import admin
from django.urls import path, include

"""
Корневой URL configuration для проекта Electronics_retail_chain.

URL patterns:
- admin/: Админ-панель Django
- api/: API endpoints приложения networknode
- api-auth/: Аутентификация для DRF
"""
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("networknode.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
