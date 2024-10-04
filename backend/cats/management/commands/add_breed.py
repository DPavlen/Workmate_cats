import json

from django.core.management.base import BaseCommand
from cats.models import Group, Breed


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            with open("data/breed.json", encoding="utf-8-sig") as f:
                breed_data = json.load(f)
                for breed in breed_data:
                    name = breed.get("name")
                    # Получаем связанный объект Group по id и связке с name
                    group_name = breed.get("group_name")
                    if group_name:
                        group, _ = Group.objects.get_or_create(name=group_name)
                        Breed.objects.get_or_create(
                            name=name,
                            group=group
                        )
        except Exception:
            raise ("Ошибка при загрузке Пород котов':")
        return (
            "Загрузка 'Пород котов' произошла успешно!"
            " Обработка файла breed.json завершена."
        )