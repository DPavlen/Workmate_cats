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


@pytest.fixture
def category():
    """
    Фикстура для создания тестовой категории с названием "Test_Group".
    Возвращает:Group: Созданный объект Group.
    Дальше используем ее ниже как предзаготовку параметра group модели Breed.
    """
    return Group.objects.create(
        name="Test_Group",
        slug="test_category_fruits",
        icon=None
    )
