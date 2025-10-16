from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Product."""

    class Meta:
        """Мета-класс для настроек сериализатора Product."""

        model = Product
        fields = ["id", "name", "model", "release_date"]


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели NetworkNode с полной информацией."""

    products = ProductSerializer(many=True, read_only=True)
    hierarchy_level = serializers.ReadOnlyField()
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    dependent_nodes_count = serializers.SerializerMethodField()

    class Meta:
        """Мета-класс для настроек сериализатора NetworkNode."""

        model = NetworkNode
        fields = [
            "id",
            "name",
            "node_type",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "supplier_name",
            "debt",
            "created_at",
            "hierarchy_level",
            "products",
            "dependent_nodes_count",
        ]
        read_only_fields = ["debt", "created_at", "hierarchy_level"]

    def get_dependent_nodes_count(self, obj):
        """Возвращает количество зависимых узлов."""

        return obj.dependent_nodes.count()


class NetworkNodeUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления модели NetworkNode.

    Исключает поле debt из возможностей обновления через API.
    """

    class Meta:
        """Мета-класс для настроек сериализатора обновления NetworkNode."""

        model = NetworkNode
        fields = [
            "id",
            "name",
            "node_type",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
        ]
