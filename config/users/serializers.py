from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    """Класс создания сериализатора для модели User"""

    class Meta:
        model = User
        fields = "__all__"