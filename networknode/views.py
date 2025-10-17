from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (OpenApiParameter, OpenApiTypes,
                                   extend_schema, extend_schema_view)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import NetworkNodeFilter
from .models import NetworkNode
from .serializer import NetworkNodeSerializer, NetworkNodeUpdateSerializer


class IsActiveEmployee(permissions.BasePermission):
    """Кастомное разрешение для проверки активности сотрудника."""

    def has_permission(self, request, view):
        """Проверяет права доступа для запроса."""
        return request.user and request.user.is_authenticated and request.user.is_active


@extend_schema_view(
    list=extend_schema(
        summary="Список узлов сети",
        description="Возвращает список всех узлов розничной сети с пагинацией.",
        parameters=[
            OpenApiParameter(
                name="country",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Фильтрация по стране",
            ),
            OpenApiParameter(
                name="city",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Фильтрация по городу",
            ),
            OpenApiParameter(
                name="node_type",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Фильтрация по типу узла (factory, retail, entrepreneur)",
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Получить узел сети",
        description="Возвращает детальную информацию об узле сети по ID.",
    ),
    create=extend_schema(
        summary="Создать узел сети", description="Создает новый узел розничной сети."
    ),
    update=extend_schema(
        summary="Обновить узел сети",
        description="Полностью обновляет информацию об узле сети.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить узел сети",
        description="Частично обновляет информацию об узле сети.",
    ),
    destroy=extend_schema(
        summary="Удалить узел сети", description="Удаляет узел сети по ID."
    ),
)
class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с моделью NetworkNode.
    Предоставляет полный набор действий для работы с узлами сети:
    list, create, retrieve, update, partial_update, destroy.
    """

    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkNodeFilter

    def get_serializer_class(self):
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
        Для update и partial_update используется сериализатор без поля debt
        """
        if self.action in ["update", "partial_update"]:
            return NetworkNodeUpdateSerializer
        return NetworkNodeSerializer

    def perform_update(self, serializer):
        """
        Выполняет обновление объекта с дополнительной валидацией.
        Запрещает обновление поля debt через API
        """
        if "debt" in serializer.validated_data:
            raise serializer.ValidationError(
                {"debt": "Обновление задолженности через API запрещено"}
            )
        serializer.save()

    @extend_schema(
        summary="Получить зависимые узлы",
        description="Возвращает список всех узлов, которые зависят от текущего узла.",
        responses={200: NetworkNodeSerializer(many=True)},
    )
    @action(detail=True, methods=["get"])
    def dependent_nodes(self, request, pk=None):
        """Получает список зависимых узлов для текущего узла."""
        node = self.get_object()
        dependent_nodes = node.dependent_nodes.all()
        serializer = NetworkNodeSerializer(dependent_nodes, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Очистить задолженность",
        description="Очищает задолженность перед поставщиком у указанного узла.",
        responses={200: None},
    )
    @action(detail=True, methods=["post"])
    def clear_debt(self, request, pk=None):
        """Кастомное действие для очистки задолженности у конкретного узла."""
        node = self.get_object()
        node.debt = 0
        node.save()
        return Response({"status": "Задолженность очищена"}, status=status.HTTP_200_OK)
