import pytest
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
from django.db.models import (
    CharField,
    DateTimeField,
    DecimalField,
    ImageField,
    ForeignKey,
    TextField
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
    """Тесты для модели породы Breed."""

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

    def test_models_fields(self):
        """
        Проверка полей модели породы котов(Breed).
        """
        fields = Breed._meta.fields
        fields_names = [field.name for field in fields]
        assert "name" in fields_names
        assert "group" in fields_names

    def test_fields_types(self):
        """
        Проверка типов полей модели породы котов(Breed).
        """
        assert isinstance(Breed._meta.get_field("name"), CharField)
        assert isinstance(Breed._meta.get_field("group"), ForeignKey)


@mark.django_db
class TestCatModel(TestCase):
    """Тесты для модели котов(Cat)."""

    def test_models_fields(self):
        """
        Проверка полей модели модели котов(Cat).
        """
        fields = Cat._meta.fields
        fields_name = [field.name for field in fields]
        assert "name" in fields_name
        assert "breed" in fields_name
        assert "owner" in fields_name
        assert "color" in fields_name
        assert "age" in fields_name
        assert "sex" in fields_name
        assert "description" in fields_name

    def test_fields_types(self):
        """
        Проверка типов полей модели котов(Cat).
        """
        assert isinstance(Cat._meta.get_field("name"), CharField)
        assert isinstance(Cat._meta.get_field("breed"), ForeignKey)
        assert isinstance(Cat._meta.get_field("owner"), ForeignKey)
        assert isinstance(Cat._meta.get_field("color"), ColorField)
        assert isinstance(Cat._meta.get_field("age"), DecimalField)
        assert isinstance(Cat._meta.get_field("sex"), CharField)
        assert isinstance(Cat._meta.get_field("description"), TextField)

    def test_age_min_validation(self):
        """
        Проверка валидации поля "Возраст кота(минимальный)" - min age.
        """
        group = Group.objects.create(name="Test_Длинношёрстные")
        breed = Breed.objects.create(name="Test_Персидская (Колорпойнт)", group=group)
        cat = Cat(
            name="Test_Барсик",
            breed=breed,
            age=0.0
        )

        with pytest.raises(ValidationError) as excinfo:
            cat.full_clean()

        assert "Минимальный возраст кота должен быть не меньше 0.1" in str(excinfo.value)

    def test_age_max_validation(self):
        """
        Проверка валидации поля "Возраст кота(максимальны)" - max age.
        """
        group = Group.objects.create(name="Test_Длинношёрстные")
        breed = Breed.objects.create(name="Test_Персидская (Колорпойнт)", group=group)
        cat = Cat(
            name="Test_Барсик",
            breed=breed,
            age=36
        )

        with pytest.raises(ValidationError) as excinfo:
            cat.full_clean()

        assert "Возраст питомца, к сожалению, не может быть больше" in str(excinfo.value)


@pytest.fixture
def group():
    """
    Фикстура для создания тестовой группы котов.
    """
    return Group.objects.create(name="Test_Короткошёрстные")


@pytest.fixture
def breed(group):
    """
    Фикстура для создания тестовой породы котов с привязкой к группе.
    """
    return Breed.objects.create(name="Test_Скоттиш фолд", group=group)


@pytest.fixture
def cat(breed):
    """
    Фикстура для создания тестового кота с привязкой к породе.
    """
    return Cat.objects.create(name="Test_Сися", breed=breed)


@pytest.mark.django_db
class TestCatPhotoModel:
    """Тесты для модели CatPhoto."""

    def test_create_cat_photo(self, cat):
        """
        Проверка создания объекта CatPhoto.
        """
        cat_photo = CatPhoto.objects.create(cat=cat, photo="test_image.jpg")
        assert cat_photo.cat == cat

    def test_str_representation(self, cat):
        """
        Проверка строкового представления модели CatPhoto.
        """
        cat_photo = CatPhoto.objects.create(cat=cat, photo="test_image.jpg")
        assert str(cat_photo) == "Test_Сися"

    def test_photo_field_required(self, cat):
        """
        Проверка валидации поля photo, которое не должно быть пустым.
        """
        cat_photo = CatPhoto(cat=cat, photo="")

        with pytest.raises(ValidationError):
            cat_photo.full_clean()


@pytest.fixture
def user():
    """
    Фикстура для создания тестового пользователя.
    """
    return CustUser.objects.create_user(
        username="pavlen",
        email="pavlen@yandex.ru",
        password="12345"
    )


@pytest.mark.django_db
class TestCatRatingModel:
    """Тесты для модели CatRating."""

    def test_create_cat_rating(self, cat, user):
        """
        Проверка создания объекта CatRating.
        """
        rating = CatRating.objects.create(cat=cat, user=user, rating=5)
        assert rating.cat == cat
        assert rating.user == user
        assert rating.rating == 5