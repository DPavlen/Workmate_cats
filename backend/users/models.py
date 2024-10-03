import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants.users import (
    USERNAME_LENGTH, EMAIL_LENGTH, ROLE_LENGTH, SEX_LENGTH, NAME_LENGTH
)
from core.validators import (
    username_validator, name_validator, validate_mobile)
from users.manager import UserManager


class CustUser(AbstractUser):
    """
    Модель пользователя с дополнительными полями.
    """

    class RoleChoises(models.TextChoices):
        """
        Определение роли юзера.
        """

        USER = "user"
        ADMIN = "admin"

    SEX_CHOICES = (
        ("М", "Male"),
        ("Ж", "Female")
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        "email address",
        max_length=EMAIL_LENGTH,
        unique=True,
    )
    username = models.CharField(
        "Логин пользователя",
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField(
        "Имя пользователя",
        max_length=NAME_LENGTH,
        validators=[name_validator],
    )
    middle_name = models.CharField(
        "Отчество",
        max_length=NAME_LENGTH,
        null=True,
        blank=True,
        validators=[name_validator],
    )
    last_name = models.CharField(
        "Фамилия пользователя",
        max_length=NAME_LENGTH,
        validators=[name_validator],
    )
    phone = models.CharField(
        "Телефон",
        max_length=20,
        null=True,
        blank=True,
        unique=True,
        validators=[validate_mobile],
    )
    birth_date = models.DateField(
        "День Рождения пользователя",
        null=True,
        blank=True,
    )
    role = models.TextField(
        "Пользовательская роль юзера",
        choices=RoleChoises.choices,
        default=RoleChoises.USER,
        max_length=ROLE_LENGTH,
    )
    sex = models.CharField(
        "Пол",
        max_length=SEX_LENGTH,
        choices=SEX_CHOICES,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-id",)

    def __str__(self):
        return self.username