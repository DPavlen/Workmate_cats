# Generated by Django 5.0.2 on 2024-10-05 19:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cats", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="cat",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cats",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец кота",
            ),
        ),
        migrations.AddField(
            model_name="catphoto",
            name="cat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to="cats.cat",
                verbose_name="Кот",
            ),
        ),
        migrations.AddField(
            model_name="catrating",
            name="cat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ratings",
                to="cats.cat",
                verbose_name="Кот",
            ),
        ),
        migrations.AddField(
            model_name="catrating",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор оценки",
            ),
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
        migrations.AlterUniqueTogether(
            name="catrating",
            unique_together={("cat", "user")},
        ),
    ]
