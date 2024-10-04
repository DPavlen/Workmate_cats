import uuid

from colorfield.fields import ColorField
from django.db import models
from model_utils.models import TimeStampedModel


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
    )
    color = ColorField(
        verbose_name="Цвет в формате HEX",
        max_length=7,
        format="hex",
        default="#808080",
        # validators=[ColorValidator],
    )
    age = models.DecimalField(
        "Возраст кота",
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Возраст указывается в годах. "
                  "Например, 1.75 = 1 год и 9 месяцев, "
                  "0.42 примерно 5 месяцев."
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
    icon = models.ImageField(
        "Фото Кота",
        upload_to="cats",
        default=None,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Кот"
        verbose_name_plural = "Коты"
        ordering = ("created",)

    def __str__(self):
        return self.name

