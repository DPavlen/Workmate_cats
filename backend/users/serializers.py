from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import CustUser


class CustomUserSerializer(UserCreateSerializer):
    """
    Сериализатор работы с пользователями, расширенный,
    для обработки дополнительных полей.
    """

    class Meta:
        model = CustUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "password": {"write_only": True, "required": False},
        }

    def create(self, validated_data):
        user = CustUser(
            email=validated_data.get("email"),
            username=validated_data.get("username"),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user


class CustomUserReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения данных у пользователей.
    """

    class Meta:
        model = CustUser
        fields = ("id", "email", "first_name", "last_name")