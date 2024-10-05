from rest_framework import serializers
from .models import Breed, Cat, Group, CatPhoto


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для группы котов."""
    class Meta:
        model = Group
        fields = ("id", "name")


class BreedSerializer(serializers.ModelSerializer):
    """Сериализатор для породы котов."""
    group_name = serializers.CharField(source="group.name", read_only=True)

    class Meta:
        model = Breed
        fields = ("id", "name", "group_name")


class CatPhotoSerializer(serializers.ModelSerializer):
    """
    Сериализатор загрузки(создания) фото и вывода информации о фото кота.
    """

    url = serializers.ImageField(source="photo", read_only=True, use_url=True)
    photo = serializers.ImageField(use_url=False, write_only=True)

    class Meta:
        model = CatPhoto
        fields = ("id", "photo", "url")


class CatSerializer(serializers.ModelSerializer):
    """Сериализатор для котов."""

    breed_display = serializers.CharField(source='breed.name', read_only=True)
    photos = CatPhotoSerializer(many=True, read_only=True)
    color = serializers.CharField(default="#808080")
    age = serializers.DecimalField(max_digits=4, decimal_places=2, default="99")
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    sex = serializers.CharField(default="Tomcat_or_Queen")

    class Meta:
        model = Cat
        fields = (
            "id",
            "name",
            "age",
            "owner_username",
            # "breed",
            "breed_display",
            "color",
            "sex",
            "description",
            "photos",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        cat = Cat(
            name=validated_data["name"],
            owner=user,
            color=validated_data["color"],
            age=validated_data.get("age"),
            sex=validated_data.get("sex"),
        )
        cat.save()
        return cat

    def validate_sex(self, value):
        """Валидатор для проверки пола кота."""
        if value not in ("Tomcat", "Queen"):
            raise serializers.ValidationError(
                "Выберите Пол кота:'Tomcat' или 'Queen'")
        return value

    def validate_age(self, value):
        """Валидатор для проверки возраста кота,
         в пределах от 0.1 до 50 лет.
        """
        if value < 0.1:
            raise serializers.ValidationError(
                f"Минимальный возраст кота должен "
                f"быть не меньше 0.1 года. Указано: {value}."
            )
        if value > 50:
            raise serializers.ValidationError(
                f"Возраст кота не может быть "
                f"больше 50 лет. Указано: {value}."
            )
        return value


class CatUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления информации
    о котах (без изменения фотографий)."""

    breed = serializers.CharField(default="Персидская (Колорпойнт)")
    color = serializers.CharField(default="#808080")
    age = serializers.DecimalField(max_digits=4, decimal_places=2)
    sex = serializers.CharField(default="Tomcat_or_Queen")
    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Cat
        fields = (
            "name",
            "age",
            "owner_username",
            "breed",
            "color",
            "sex",
            "description"
        )
        read_only_fields = ("owner_username",)

    def validate_breed(self, value):
        """
        Проверка на существование породы по имени.
        """
        try:
            breed = Breed.objects.get(name=value)
        except Breed.DoesNotExist:
            raise serializers.ValidationError(
                f"Порода с именем '{value}' не найдена. "
                f"Ознакомиться с доступными породами в разделе: "
                f" breeds (Работа с породами котов)"
                f" по адресу: /api/breeds/ Получить список всех пород котов"
            )
        return breed

    def validate_sex(self, value):
        """Валидатор для проверки пола кота."""
        if value not in ("Tomcat", "Queen"):
            raise serializers.ValidationError(
                "Выберите Пол кота:'Tomcat' или 'Queen'")
        return value

    def validate_age(self, value):
        """
        Валидатор для проверки возраста кота.
        Возраст должен быть в пределах от 0.1 до 50 лет.
        """
        if value < 0.1:
            raise serializers.ValidationError(
                f"Минимальный возраст кота должен быть не меньше 0.1 года. Указано: {value}."
            )
        if value > 50:
            raise serializers.ValidationError(
                f"Возраст кота не может быть больше 50 лет. Указано: {value}."
            )
        return value

    def update(self, instance, validated_data):
        """
        Метод обновления кота без изменения фотографий.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)
        instance.color = validated_data.get("color", instance.color)
        instance.description = validated_data.get("description", instance.description)
        instance.breed = validated_data.get("breed", instance.breed)
        instance.save()
        return instance