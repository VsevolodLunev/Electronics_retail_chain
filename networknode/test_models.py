from datetime import date

import pytest

from .models import NetworkNode, Product


@pytest.mark.django_db
class TestNetworkNodeModel:
    """
    Тесты для модели NetworkNode.
    """

    def test_network_node_creation(self):
        """Тест создания узла сети."""
        factory = NetworkNode.objects.create(
            name="Главный завод",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
            debt=1000.00,
        )

        assert factory.name == "Главный завод"
        assert factory.node_type == "factory"
        assert factory.hierarchy_level == 0

    def test_hierarchy_level(self):
        """Тест вычисления уровня иерархии."""
        factory = NetworkNode.objects.create(
            name="Главный завод",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
        )

        retail = NetworkNode.objects.create(
            name="Розничная сеть 1",
            node_type="retail",
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский",
            house_number="2",
            supplier=factory,
        )

        assert factory.hierarchy_level == 0
        assert retail.hierarchy_level == 1

    def test_str_representation(self):
        """Тест строкового представления."""
        factory = NetworkNode.objects.create(
            name="Главный завод",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
        )

        retail = NetworkNode.objects.create(
            name="Розничная сеть 1",
            node_type="retail",
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский",
            house_number="2",
            supplier=factory,
        )

        assert str(factory) == "Завод: Главный завод"
        assert str(retail) == "Розничная сеть: Розничная сеть 1"

    def test_dependent_nodes_relationship(self):
        """Тест отношения dependent_nodes."""
        factory = NetworkNode.objects.create(
            name="Главный завод",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
        )

        retail = NetworkNode.objects.create(
            name="Розничная сеть 1",
            node_type="retail",
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский",
            house_number="2",
            supplier=factory,
        )

        dependent_nodes = factory.dependent_nodes.all()
        assert dependent_nodes.count() == 1
        assert dependent_nodes[0] == retail

    def test_dependent_nodes_count_property(self):
        """Тест свойства dependent_nodes_count."""
        factory = NetworkNode.objects.create(
            name="Главный завод",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Лениna",
            house_number="1",
        )

        NetworkNode.objects.create(
            name="Розничная сеть 1",
            node_type="retail",
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский",
            house_number="2",
            supplier=factory,
        )

        # У завода должен быть 1 зависимый узел
        assert factory.dependent_nodes.count() == 1


@pytest.mark.django_db
class TestProductModel:
    """
    Тесты для модели Product.
    """

    def test_product_creation(self):
        """Тест создания продукта."""
        node = NetworkNode.objects.create(
            name="Тестовый узел",
            node_type="retail",
            email="test@example.com",
            country="Россия",
            city="Москва",
            street="Тестовая",
            house_number="1",
        )

        product = Product.objects.create(
            name="Смартфон",
            model="X100",
            release_date=date(2023, 1, 1),
            network_node=node,
        )

        assert product.name == "Смартфон"
        assert product.model == "X100"
        assert product.network_node == node

    def test_str_representation(self):
        """Тест строкового представления."""
        node = NetworkNode.objects.create(
            name="Тестовый узел",
            node_type="retail",
            email="test@example.com",
            country="Россия",
            city="Москва",
            street="Тестовая",
            house_number="1",
        )

        product = Product.objects.create(
            name="Смартфон",
            model="X100",
            release_date=date(2023, 1, 1),
            network_node=node,
        )

        assert str(product) == "Смартфон (X100)"
