# Generated by Django 5.0.2 on 2024-10-04 10:58

import colorfield.fields
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Breed",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название породы кота"
                    ),
                ),
            ],
            options={
                "verbose_name": "Порода кота",
                "verbose_name_plural": "Породы котов",
                "ordering": ("created",),
            },
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100,
                        unique=True,
                        verbose_name="Название группы котов",
                    ),
                ),
            ],
            options={
                "verbose_name": "Группа кота",
                "verbose_name_plural": "Группы котов",
                "ordering": ("created",),
            },
        ),
        migrations.CreateModel(
            name="Cat",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Имя кота")),
                (
                    "color",
                    colorfield.fields.ColorField(
                        default="#808080",
                        image_field=None,
                        max_length=7,
                        samples=None,
                        unique=True,
                        verbose_name="Цвет в формате HEX",
                    ),
                ),
                (
                    "age",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Возраст указывается в годах. Например, 1.75 = 1 год и 9 месяцев, 0.42 примерно 5 месяцев.",
                        max_digits=4,
                        null=True,
                        verbose_name="Возраст кота",
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        blank=True,
                        choices=[("Tomcat", "Кот"), ("Queen", "Кошка")],
                        max_length=10,
                        null=True,
                        verbose_name="Пол кота",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Текст описания кота"
                    ),
                ),
                (
                    "icon",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="cats",
                        verbose_name="Фото Кота",
                    ),
                ),
                (
                    "breed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cats",
                        to="cats.breed",
                        verbose_name="Порода кота",
                    ),
                ),
            ],
            options={
                "verbose_name": "Кот",
                "verbose_name_plural": "Коты",
                "ordering": ("created",),
            },
        ),
        migrations.AddField(
            model_name="breed",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="breeds",
                to="cats.group",
                verbose_name="Группа котов",
            ),
        ),
    ]
