from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date
from .models import NetworkNode, Product
from .serializer import NetworkNodeSerializer


class NetworkNodeModelTest(TestCase):
    """Тесты для модели NetworkNode."""

    def setUp(self):
        """Настройка тестовых данных."""
        self.factory = NetworkNode.objects.create(
            name="Главный завод",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
            debt=1000.00,
        )

        self.retail_chain = NetworkNode.objects.create(
            name="Розничная сеть 1",
            node_type="retail",
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский",
            house_number="2",
            supplier=self.factory,
            debt=500.00,
        )

    def test_network_node_creation(self):
        """Тест создания узла сети."""
        self.assertEqual(self.factory.name, "Главный завод")
        self.assertEqual(self.factory.node_type, "factory")
        self.assertEqual(self.factory.hierarchy_level, 0)

    def test_hierarchy_level(self):
        """Тест вычисления уровня иерархии."""
        self.assertEqual(self.factory.hierarchy_level, 0)
        self.assertEqual(self.retail_chain.hierarchy_level, 1)

    def test_str_representation(self):
        """Тест строкового представления."""
        self.assertEqual(str(self.factory), "Завод: Главный завод")
        self.assertEqual(str(self.retail_chain), "Розничная сеть: Розничная сеть 1")

    def test_dependent_nodes_relationship(self):
        """Тест отношения dependent_nodes."""
        dependent_nodes = self.factory.dependent_nodes.all()
        self.assertEqual(dependent_nodes.count(), 1)
        self.assertEqual(dependent_nodes[0], self.retail_chain)

    def test_dependent_nodes_count_property(self):
        """Тест свойства dependent_nodes_count."""
        # У завода должен быть 1 зависимый узел
        self.assertEqual(self.factory.dependent_nodes.count(), 1)

        # У розничной сети не должно быть зависимых узлов
        self.assertEqual(self.retail_chain.dependent_nodes.count(), 0)

    def test_serializer_includes_dependent_nodes_count(self):  # ← НОВЫЙ тест
        """Тест что сериализатор включает dependent_nodes_count."""
        serializer = NetworkNodeSerializer(self.factory)
        data = serializer.data
        self.assertIn("dependent_nodes_count", data)
        self.assertEqual(data["dependent_nodes_count"], 1)


class ProductModelTest(TestCase):
    """Тесты для модели Product."""

    def setUp(self):
        """Настройка тестовых данных."""
        self.node = NetworkNode.objects.create(
            name="Тестовый узел",
            node_type="retail",
            email="test@example.com",
            country="Россия",
            city="Москва",
            street="Тестовая",
            house_number="1",
        )

        self.product = Product.objects.create(
            name="Смартфон",
            model="X100",
            release_date=date(2023, 1, 1),
            network_node=self.node,
        )

    def test_product_creation(self):
        """Тест создания продукта."""
        self.assertEqual(self.product.name, "Смартфон")
        self.assertEqual(self.product.model, "X100")
        self.assertEqual(self.product.network_node, self.node)

    def test_str_representation(self):
        """Тест строкового представления."""
        self.assertEqual(str(self.product), "Смартфон (X100)")


class NetworkNodeAPITest(APITestCase):
    """Тесты для API NetworkNode."""

    def setUp(self):
        """Настройка тестовых данных."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", is_active=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.factory = NetworkNode.objects.create(
            name="Главный завод",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
        )

        # Создаем зависимый узел для тестирования
        self.retail_chain = NetworkNode.objects.create(
            name="Розничная сеть 1",
            node_type="retail",
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский",
            house_number="2",
            supplier=self.factory,
        )

    def test_list_network_nodes(self):
        """Тест получения списка узлов сети."""
        response = self.client.get("/api/network-nodes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем что ответ содержит результаты
        self.assertIn("results", response.data)

    def test_create_network_node(self):
        """Тест создания узла сети."""
        data = {
            "name": "Новая розничная сеть",
            "node_type": "retail",
            "email": "new@example.com",
            "country": "Россия",
            "city": "Казань",
            "street": "Баумана",
            "house_number": "10",
            "supplier": self.factory.id,
        }
        response = self.client.post("/api/network-nodes/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Новая розничная сеть")

    def test_filter_by_country(self):
        """Тест фильтрации по стране."""
        response = self.client.get("/api/network-nodes/?country=Россия")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_filter_by_city(self):
        """Тест фильтрации по городу."""
        response = self.client.get("/api/network-nodes/?city=Москва")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_dependent_nodes_count_in_response(self):
        """Тест что dependent_nodes_count присутствует в ответе API."""
        response = self.client.get(f"/api/network-nodes/{self.factory.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("dependent_nodes_count", response.data)
        # У завода должен быть 1 зависимый узел
        self.assertEqual(response.data["dependent_nodes_count"], 1)

    def test_dependent_nodes_endpoint(self):
        """Тест endpoint для получения зависимых узлов."""
        response = self.client.get(
            f"/api/network-nodes/{self.factory.id}/dependent_nodes/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Розничная сеть 1")

    def test_unauthenticated_access(self):
        """Тест доступа без аутентификации."""
        client = APIClient()  # клиент без аутентификации
        response = client.get("/api/network-nodes/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProductAPITest(APITestCase):
    """Тесты для API Product."""

    def setUp(self):
        """Настройка тестовых данных."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", is_active=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.node = NetworkNode.objects.create(
            name="Тестовый узел",
            node_type="retail",
            email="test@example.com",
            country="Россия",
            city="Москва",
            street="Тестовая",
            house_number="1",
        )

        self.product = Product.objects.create(
            name="Смартфон",
            model="X100",
            release_date=date(2023, 1, 1),
            network_node=self.node,
        )

    def test_products_in_network_node(self):
        """Тест что продукты отображаются в узле сети."""
        response = self.client.get(f"/api/network-nodes/{self.node.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("products", response.data)
        self.assertEqual(len(response.data["products"]), 1)
        self.assertEqual(response.data["products"][0]["name"], "Смартфон")
