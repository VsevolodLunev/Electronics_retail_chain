import django_filters

from .models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    """Фильтр по стране, городу и типу узла для модели NetworkNode."""

    country = django_filters.CharFilter(
        field_name="country",
        lookup_expr="iexact",
        help_text="Фильтрация по стране (точное совпадение, без учета регистра)",
    )
    city = django_filters.CharFilter(
        field_name="city",
        lookup_expr="iexact",
        help_text="Фильтрация по городу (точное совпадение, без учета регистра)",
    )

    class Meta:
        """Мета-класс для настроек фильтра."""

        model = NetworkNode
        fields = ["country", "city", "node_type"]
