from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers


from users.models import CustUser


class CustomUserSerializer(UserCreateSerializer):
    """
    Сериализатор работы с пользователями, расширенный,
    для обработки дополнительных полей.
    """

    email = serializers.EmailField(min_length=6, max_length=70)

    class Meta:
        model = CustUser
        fields = (
            "email",
            "id",
            "username",
            "password",
        )
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
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

    def validate_email(self, value):
        if CustUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует"
            )
        return value


class CustomUserUpdateSerializer(UserSerializer):
    """
    Сериализатор обновления пользователей.
    Используется для просмотра и обновления данных существующего пользователя.
    Атрибуты:
        - Meta: Класс метаданных для определения модели и полей сериализатора.
    """

    phone = serializers.CharField(default="+79167775544", required=False)
    first_name = serializers.CharField(min_length=2, max_length=50, required=False)
    middle_name = serializers.CharField(min_length=2, max_length=50, required=False)
    last_name = serializers.CharField(min_length=2, max_length=50, required=False)
    sex = serializers.CharField(default="М_или_Ж", required=False)

    class Meta(UserSerializer.Meta):
        model = CustUser
        fields = (
            "id",
            "username",
            "email",
            "phone",
            "first_name",
            "middle_name",
            "last_name",
            "sex",
        )
        read_only_fields = (
            "id",
            "email",
            "username",
        )

    def validate_phone(self, value):
        """
        Проверка уникальности телефона при обновлении.
        """
        if value:
            if (
                    CustUser.objects.exclude(id=self.instance.id)
                            .filter(phone=value)
                            .exists()
            ):
                raise serializers.ValidationError(
                    "Телефонный номер уже используется. Введите другой!"
                )

        return value

    def validate_sex(self, value):
        """
        Проверка ввода обновления пола.
        """

        if value not in (choice[0] for choice in CustUser.SEX_CHOICES):
            raise serializers.ValidationError("Выберите пол 'М' или 'Ж'.")
        return value

    def update(self, instance, validated_data):
        """
        Обновление пользователя с валидацией из моделей.
        Запускаем полную проверку данных модели, вызывая метод full_clean()
        Исключения: serializers.ValidationError:
        Возникает при ошибке валидации на уровне модели.
        """
        instance.phone = validated_data.get("phone", instance.phone)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.middle_name = validated_data.get("middle_name", instance.middle_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.sex = validated_data.get("sex", instance.sex)

        try:
            instance.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        instance.save()
        return instance


class CustomUserReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения данных у пользователей.
    """

    class Meta:
        model = CustUser
        fields = ("id", "email", "username", "first_name", "last_name")