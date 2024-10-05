import re
from re import search

from django.core.exceptions import ValidationError


def username_validator(username):
    """Валидация для поля 'Логин пользователя' модели User."""
    if username == "me":
        raise ValidationError("Нельзя использовать имя пользователя me")

    if not search(r"^[a-zA-Z][a-zA-Z0-9-_.]{1,150}$", username):
        raise ValidationError("В логине Пользователя используются недопустимые символы")


def name_validator(name):
    """Общий валидатор: Имя пользователя
    и Фамилия пользователя модели User."""


    if not search(r"^[A-Za-zА-Яа-я0-9]{1,150}$", name):
        raise ValidationError("В поле пользователя используются недопустимые символы")


def validate_mobile(value):
    """Валидация для поля "Телефон"."""
    rule = re.compile(r"^\+?[7-8]?[0-9]{10}$")
    if not rule.search(value):
        raise ValidationError("Неверный мобильный номер.")


def validate_color(value):
    """
    Валидация поля color-Цвет Тега в формате HEX и его соответсвие.
    """
    regex = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
    max_length = 7
    message = (
        f"Введенное значение не является цветом в формате HEX! "
        f"Длина не более {max_length} символов"
    )

    if not regex.match(value):
        raise ValueError(message)