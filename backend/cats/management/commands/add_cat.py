import json
import random
from django.core.management.base import BaseCommand
from cats.models import Group, Breed, Cat


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            with open("data/cat.json", encoding="utf-8-sig") as f:
                cat_data = json.load(f)
                for cat in cat_data:
                    name = cat.get("name")
                    breed_name = cat.get("breed")
                    color = cat.get("color")
                    age = cat.get("age")
                    sex = cat.get("sex")
                    description = cat.get("description")

                    # Получаем связанный объект Breed по id и связке с name
                    breed = Breed.objects.get(name=breed_name)

                    Cat.objects.get_or_create(
                        name=name,
                        breed=breed,
                        color=color,
                        age=age,
                        sex=sex,
                        description=description
                    )
        except Exception:
            raise ("Ошибка при загрузке Котов':")
        return (
            "Загрузка 'Котов и Кошек' произошла успешно!"
            " Обработка файла cat.json завершена."
        )