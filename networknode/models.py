from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class NetworkNode(models.Model):
    """Модель для представления звена сети электроники."""

    NODE_TYPES = [
        ("factory", "Завод"),
        ("retail", "Розничная сеть"),
        ("entrepreneur", "Индивидуальный предприниматель"),
    ]
    name = models.CharField(max_length=255, verbose_name="Название")
    node_type = models.CharField(
        max_length=20, choices=NODE_TYPES, verbose_name="Тип звена"
    )
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=255, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dependent_nodes",
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=0.00,
        verbose_name="Задолженность перед поставщиком",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        """Мета-класс для настроек модели."""

        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ["-created_at"]

    def __str__(self):
        """Строковое представление объекта."""
        return f"{self.get_node_type_display()}: {self.name}"

    @property
    def hierarchy_level(self):
        """
        Вычисляет уровень иерархии звена в сети.
        Returns:
            int: Уровень иерархии (0 для завода, 1+ для остальных)
        """
        if self.supplier is None:
            return 0
        return self.supplier.hierarchy_level + 1


class Product(models.Model):
    """Модель для представления продукта в сети."""

    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")
    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Звено сети",
    )

    class Meta:
        """Мета-класс для настроек модели."""

        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        """Строковое представление объекта."""
        return f"{self.name} ({self.model})"
