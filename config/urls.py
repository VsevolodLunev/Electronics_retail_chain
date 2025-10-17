from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

"""
Корневой URL configuration для проекта Electronics_retail_chain.

URL patterns:
- admin/: Админ-панель Django
- api/: API endpoints приложения networknode
- api-auth/: Аутентификация для DRF
- api/schema/: Swagger/OpenAPI схема
- api/docs/: Swagger UI документация
- api/redoc/: ReDoc документация
"""
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("networknode.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
