from datetime import date

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .models import NetworkNode, Product


@pytest.mark.django_db
class TestNetworkNodeAPI:
    """
    Тесты для API NetworkNode.
    """

    @pytest.fixture
    def api_client(self):
        """Фикстура для API клиента."""
        return APIClient()

    @pytest.fixture
    def user(self):
        """Фикстура для тестового пользователя."""
        return User.objects.create_user(
            username="testuser", password="testpass123", is_active=True
        )

    @pytest.fixture
    def factory_node(self):
        """Фикстура для тестового завода."""
        return NetworkNode.objects.create(
            name="Главный завод",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
        )

    @pytest.fixture
    def retail_node(self, factory_node):
        """Фикстура для тестовой розничной сети."""
        return NetworkNode.objects.create(
            name="Розничная сеть 1",
            node_type="retail",
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский",
            house_number="2",
            supplier=factory_node,
        )

    def test_list_network_nodes(self, api_client, user, factory_node):
        """Тест получения списка узлов сети."""
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/network-nodes/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data

    def test_create_network_node(self, api_client, user, factory_node):
        """Тест создания узла сети."""
        api_client.force_authenticate(user=user)
        data = {
            "name": "Новая розничная сеть",
            "node_type": "retail",
            "email": "new@example.com",
            "country": "Россия",
            "city": "Казань",
            "street": "Баумана",
            "house_number": "10",
            "supplier": factory_node.id,
        }
        response = api_client.post("/api/network-nodes/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Новая розничная сеть"

    def test_filter_by_country(self, api_client, user, factory_node):
        """Тест фильтрации по стране."""
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/network-nodes/?country=Россия")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data

    def test_unauthenticated_access(self, api_client):
        """Тест доступа без аутентификации."""
        response = api_client.get("/api/network-nodes/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_dependent_nodes_endpoint(
        self, api_client, user, factory_node, retail_node
    ):
        """Тест endpoint для получения зависимых узлов."""
        api_client.force_authenticate(user=user)
        response = api_client.get(
            f"/api/network-nodes/{factory_node.id}/dependent_nodes/"
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Розничная сеть 1"


@pytest.mark.django_db
class TestProductAPI:
    """
    Тесты для API Product.
    """

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="testuser", password="testpass123", is_active=True
        )

    @pytest.fixture
    def network_node(self):
        return NetworkNode.objects.create(
            name="Тестовый узел",
            node_type="retail",
            email="test@example.com",
            country="Россия",
            city="Москва",
            street="Тестовая",
            house_number="1",
        )

    @pytest.fixture
    def product(self, network_node):
        return Product.objects.create(
            name="Смартфон",
            model="X100",
            release_date=date(2023, 1, 1),
            network_node=network_node,
        )

    def test_products_in_network_node(self, api_client, user, network_node, product):
        """Тест что продукты отображаются в узле сети."""
        api_client.force_authenticate(user=user)
        response = api_client.get(f"/api/network-nodes/{network_node.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert "products" in response.data
        assert len(response.data["products"]) == 1
        assert response.data["products"][0]["name"] == "Смартфон"
