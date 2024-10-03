from rest_framework import serializers
from .models import Breed, Cat, Group


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


class CatSerializer(serializers.ModelSerializer):
    """Сериализатор для котов."""
    breed = BreedSerializer(read_only=True)

    class Meta:
        model = Cat
        fields = (
            "id",
            "name",
            "age",
            "breed",
            "color",
            "description"
        )
