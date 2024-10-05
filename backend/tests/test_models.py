import pytest
from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    DateTimeField,
    DecimalField,
    ImageField,
    ForeignKey,
    PositiveSmallIntegerField
)
from django.test import TestCase
from gunicorn.config import User
from pytest import mark
from pytest_django.asserts import assertRaisesMessage

from users.models import CustUser
from cats.models import (
    Group,
    Breed,
    Cat,
    CatPhoto,
    CatRating
)


@pytest.mark.django_db
class TestBreedModel:
    """Тесты для модели Breed."""

    @pytest.fixture
    def group(self):
        """
        Фикстура для создания тестовой группы с названием "Test_Длинношёрстные".
        Возвращает: Group: Созданный объект Group.
        """
        return Group.objects.create(
            name="Test_Длинношёрстные",
        )

    @pytest.fixture
    def breed(self, group):
        """
        Фикстура для создания тестовой породы, связанной с группой.
        Возвращает: Breed: Созданный объект Breed.
        """
        return Breed.objects.create(
            name="Test_Гималайская кошка",
            group=group,
        )

    def test_str_representation(self, breed):
        """
        Проверка строкового представления модели Breed.
        """
        assert str(breed) == "Test_Гималайская кошка"

    def test_group_relationship(self, breed, group):
        """
        Проверка, что порода связана с группой.
        """
        assert breed.group == group
