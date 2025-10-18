from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import NetworkNode, Product


class ProductInline(admin.TabularInline):
    """Inline-админка для отображения продуктов внутри узла сети."""

    model = Product
    extra = 1


class DependentNodesInline(admin.TabularInline):
    """Inline-админка для отображения зависимых узлов(dependent_nodes)."""

    model = NetworkNode
    fk_name = "supplier"
    extra = 1
    fields = ["name", "node_type", "email", "city"]
    readonly_fields = ["name", "node_type", "email", "city"]


class CityFilter(admin.SimpleListFilter):
    """Кастомный фильтр для админ-панели по городу."""

    title = "Город"
    parameter_name = "city"

    def lookups(self, request, model_admin):
        """Возвращает список доступных значений для фильтра."""
        cities = NetworkNode.objects.values_list("city", flat=True).distinct()
        return [(city, city) for city in cities if city]

    def queryset(self, request, queryset):
        """Фильтрует queryset по выбранному значению."""
        if self.value():
            return queryset.filter(city=self.value())
        return queryset


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Админ-класс для модели NetworkNode."""

    list_display = [
        "name",
        "node_type",
        "email",
        "city",
        "supplier_link",
        "debt",
        "created_at",
        "hierarchy_level_display",
        "dependent_nodes_count",
    ]
    list_filter = ["node_type", "country", CityFilter, "created_at"]
    search_fields = ["name", "email", "city"]
    inlines = [ProductInline]
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        """Создает HTML-ссылку на страницу поставщика в админке."""
        if obj.supplier:
            url = reverse(
                "admin:networknode_networknode_change", args=[obj.supplier.id]
            )
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"

    def hierarchy_level_display(self, obj):
        """Отображает уровень иерархии в админке."""
        return obj.hierarchy_level

    hierarchy_level_display.short_description = "Уровень иерархии"

    def dependent_nodes_count(self, obj):
        """Отображает количество зависимых узлов."""
        return obj.dependent_nodes.count()

    dependent_nodes_count.short_description = "Зависимые узлы"

    def clear_debt(self, request, queryset):
        """Admin action для очистки задолженности у выбранных объектов."""
        updated_count = queryset.update(debt=0)
        self.message_user(
            request, f"Задолженность очищена для {updated_count} объектов"
        )

    clear_debt.short_description = "Очистить задолженность перед поставщиком"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-класс для модели Product."""

    list_display = ["name", "model", "release_date", "network_node"]
    list_filter = ["release_date", "network_node"]
    search_fields = ["name", "model"]
