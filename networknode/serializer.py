from rest_framework import serializers

from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Product."""

    class Meta:
        """Мета-класс для настроек сериализатора Product."""

        model = Product
        fields = ["id", "name", "model", "release_date"]

    def create(self, validated_data):
        """Создание нового продукта."""
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновление существующего продукта."""
        instance.name = validated_data.get("name", instance.name)
        instance.model = validated_data.get("model", instance.model)
        instance.release_date = validated_data.get(
            "release_date", instance.release_date
        )
        instance.save()
        return instance


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

    def create(self, validated_data):
        """Создание нового узла сети."""
        return NetworkNode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновление существующего узла сети."""
        # Запрещаем обновление поля debt через API
        if "debt" in validated_data:
            raise serializers.ValidationError(
                {"debt": "Обновление задолженности через API запрещено"}
            )
        instance.name = validated_data.get("name", instance.name)
        instance.node_type = validated_data.get("node_type", instance.node_type)
        instance.email = validated_data.get("email", instance.email)
        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)
        instance.street = validated_data.get("street", instance.street)
        instance.house_number = validated_data.get(
            "house_number", instance.house_number
        )
        instance.supplier = validated_data.get("supplier", instance.supplier)
        instance.save()
        return instance

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

    def update(self, instance, validated_data):
        """Обновление существующего узла сети."""
        instance.name = validated_data.get("name", instance.name)
        instance.node_type = validated_data.get("node_type", instance.node_type)
        instance.email = validated_data.get("email", instance.email)
        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)
        instance.street = validated_data.get("street", instance.street)
        instance.house_number = validated_data.get(
            "house_number", instance.house_number
        )
        instance.supplier = validated_data.get("supplier", instance.supplier)
        instance.save()
        return instance
