import json
from django.core.management.base import BaseCommand
from cats.models import Group, Breed, Cat
from users.models import CustUser


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
                    owner_username = cat.get("owner")

                    # Получаем связанный объект Breed по id и связке с name
                    breed = Breed.objects.get(name=breed_name)

                    # Получаем владельца по username, если он указан в файле
                    owner = None
                    if owner_username:
                        owner = CustUser.objects.get(username=owner_username)
                    else:
                        # Можно указать владельца по умолчанию, если он не указан в данных
                        owner = CustUser.objects.get(username="default_owner")

                    Cat.objects.get_or_create(
                        name=name,
                        breed=breed,
                        color=color,
                        age=age,
                        sex=sex,
                        description=description,
                        owner=owner
                    )

        except Breed.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "Ошибка: Указанная порода не найдена в базе данных."))
        except CustUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "Ошибка: Указанный владелец не найден в базе данных."))
        except Exception:
            raise ("Ошибка при загрузке Котов':")
        return (
            "Загрузка 'Котов и Кошек' произошла успешно!"
            " Обработка файла cat.json завершена."
        )