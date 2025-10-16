from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode
from .serializer import NetworkNodeSerializer, NetworkNodeUpdateSerializer
from .filters import NetworkNodeFilter


class IsActiveEmployee(permissions.BasePermission):
    """Кастомное разрешение для проверки активности сотрудника."""

    def has_permission(self, request, view):
        """Проверяет права доступа для запроса."""

        return request.user and request.user.is_authenticated and request.user.is_active


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

    @action(detail=True, methods=["get"])
    def dependent_nodes(self, request, pk=None):
        """Получает список зависимых узлов для текущего узла."""

        node = self.get_object()
        dependent_nodes = node.dependent_nodes.all()
        serializer = NetworkNodeSerializer(dependent_nodes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def clear_debt(self, request, pk=None):
        """Кастомное действие для очистки задолженности у конкретного узла."""

        node = self.get_object()
        node.debt = 0
        node.save()
        return Response({"status": "Задолженность очищена"})
