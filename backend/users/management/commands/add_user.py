import json
from django.core.management.base import BaseCommand
from users.models import CustUser
from faker import Faker

fake = Faker(["ru_RU"])


class Command(BaseCommand):
    help = "Загрузка пользователей из файла user.json"

    def handle(self, *args, **kwargs):
        try:
            with open("data/user.json", encoding="utf-8-sig") as f:
                users_data = json.load(f)
                for user in users_data:
                    email = user.get("email")
                    username = user.get("username")
                    role = user.get("role")
                    sex = user.get("sex")
                    password = user.get("password")
                    first_name = user.get("first_name")
                    last_name = user.get("last_name")
                    # Создаем или обновляем пользователя
                    user_obj, created = CustUser.objects.get_or_create(
                        email=email,
                        username=username,
                        defaults={
                            "role": role,
                            "sex": sex
                        },
                        first_name=first_name,
                        last_name=last_name,
                    )
                    # Если пользователь только создан, устанавливаем пароль
                    if created:
                        user_obj.set_password(password)
                        user_obj.save()

            self.stdout.write(self.style.SUCCESS(
                "Загрузка пользователей завершена успешно!"
            ))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка при загрузке пользователей: {e}"))