from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import FilterSet

from electronics.models import NetworkObject, Product
from electronics.serializers import (
    NetworkObjectDetailSerializer,
    NetworkObjectSerializer,
    ProductSerializer,
    NetworkObjectCreateSerializer,
    NetworkObjectUpdateSerializer,
)
from users.permissions import IsActiveAndIsStaff


class ProductViewSet(ModelViewSet):
    """
    Класс настройки CRUD для модели Product с помощью метода ViewSet
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "model", "description"]
    ordering_fields = ["name", "launch_date"]

    def get_permissions(self):
        """
        Метод для проверки доступа к функционалу сайта в зависимости от роли пользователя.
        """
        if self.action in ["create", "retrieve", "list", "partial_update", "update"]:
            self.permission_classes = (IsActiveAndIsStaff,)
        elif self.action == "destroy":
            self.permission_classes = (IsAdminUser,)

        return super().get_permissions()


class NetworkObjectViewSet(ModelViewSet):
    """
    Класс настройки CRUD для модели NetworkObject с помощью метода ViewSet
    """

    queryset = NetworkObject.objects.all()
    filter_backends = [SearchFilter, OrderingFilter, FilterSet]
    search_fields = ["name", "country", "town", "street", "phone_number"]
    ordering_fields = ["name", "time_of_creation"]
    filterset_fields = {"country": ("exact", "contains"), "provider": ("exact", "contains")}

    def get_serializer_class(self):
        """
        Метод получения сериализатора в зависимости от запроса
        (вывод всего списка или просмотр одного объекта).
        """
        if self.action == "retrieve":
            return NetworkObjectDetailSerializer
        elif self.action == "create":
            return NetworkObjectCreateSerializer
        elif self.action in ["partial_update", "update"]:
            return NetworkObjectUpdateSerializer

        return NetworkObjectSerializer

    def get_permissions(self):
        """
        Метод для проверки доступа к функционалу сайта в зависимости от роли пользователя.
        """
        if self.action in ["create", "retrieve", "list"]:
            self.permission_classes = (IsActiveAndIsStaff,)
        elif self.action in ["partial_update", "update"]:
            self.permission_classes = (IsActiveAndIsStaff,)
        elif self.action == "destroy":
            self.permission_classes = (IsAdminUser,)

        return super().get_permissions()
