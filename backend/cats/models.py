import uuid

from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from model_utils.models import TimeStampedModel

from core.validators import validate_color
from users.models import CustUser


class Group(TimeStampedModel):
    """Модель группы котов."""
    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        "Название группы котов",
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = "Группа кота"
        verbose_name_plural = "Группы котов"
        ordering = ("created",)

    def __str__(self):
        return self.name


class Breed(TimeStampedModel):
    """Модель породы котов."""
    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        "Название породы кота",
        max_length=100,
        unique=True,
    )
    group = models.ForeignKey(
        Group,
        verbose_name="Группа котов",
        on_delete=models.CASCADE,
        related_name="breeds"
    )

    class Meta:
        verbose_name = "Порода кота"
        verbose_name_plural = "Породы котов"
        ordering = ("created",)

    def __str__(self):
        return self.name


class Cat(TimeStampedModel):
    """Модель котов."""
    SEX_CHOICES = (
        ("Tomcat", "Кот"),
        ("Queen", "Кошка")
    )
    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        "Имя кота",
        max_length=50,
    )
    breed = models.ForeignKey(
        Breed,
        verbose_name="Порода кота",
        on_delete=models.CASCADE,
        related_name="cats",
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        CustUser,
        on_delete=models.CASCADE,
        related_name="cats",
        verbose_name="Владелец кота",
        null=True,
        blank=True,
    )
    color = ColorField(
        verbose_name="Цвет в формате HEX",
        max_length=7,
        format="hex",
        default="#808080",
        validators=[validate_color],
    )
    age = models.DecimalField(
        "Возраст кота",
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Возраст указывается в годах. "
                  "Например, 1.75 = 1 год и 9 месяцев, "
                  "0.42 примерно 5 месяцев.",
        validators=[
            MinValueValidator(
                0.1,
                message="Минимальный возраст кота "
                        "должен быть не меньше "
                        f"{0.1} ",
            ),
            MaxValueValidator(
                35,
                message="Возраст питомца, к сожалению, "
                        "не может быть больше"
                        f" {35}."
            ),
        ],
    )
    sex = models.CharField(
        max_length=10,
        verbose_name="Пол кота",
        choices=SEX_CHOICES,
        null=True,
        blank=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Текст описания кота"
    )

    class Meta:
        verbose_name = "Кот"
        verbose_name_plural = "Коты"
        ordering = ("created",)

    def __str__(self):
        return self.name


class CatPhoto(models.Model):
    """Модель фото кота."""

    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    cat = models.ForeignKey(
        Cat,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Кот"
    )
    photo = models.ImageField("Фото кота")

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
        ordering = ("cat__name",)

    def __str__(self):
        return self.cat.name


class CatRating(models.Model):
    """Модель подсчета рейтинга котов."""
    cat = models.ForeignKey(
        Cat,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="Кот"
    )
    user = models.ForeignKey(
        CustUser,
        on_delete=models.CASCADE,
        verbose_name="Автор оценки"
    )
    rating = models.PositiveIntegerField(
        verbose_name="Оценка коту/кошки",
        validators=[
            MinValueValidator(1), MaxValueValidator(5)
        ]
    )

    class Meta:
        verbose_name = "Оценка кота"
        verbose_name_plural = "Оценки котов"
        unique_together = ("cat", "user")

    def __str__(self):
        return (f"Оценка {self.rating} для "
                f"{self.cat.name} от {self.user.username}")