import json

from django.core.management.base import BaseCommand
from cats.models import Group


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            with open("data/group.json", encoding="utf-8-sig") as f:
                group_data = json.load(f)
                for group in group_data:
                    name = group.get("name")
                    Group.objects.get_or_create(name=name)
        except Exception:
            raise ("Ошибка при загрузке Групп котов':")
        return (
            "Загрузка 'Групп котов' произошла успешно!"
            " Обработка файла group.json завершена."
        )