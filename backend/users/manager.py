from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Менеджер пользователей.
    Этот менеджер обеспечивает создание и управление пользователями в системе.
    Methods:
        - _create_user(email, password, **extra_fields): Создает и сохраняет
        пользователя с заданным email и паролем.
        - create_user(email, password=None, **extra_fields): Создает и
        сохраняет обычного пользователя.
        - create_superuser(email, password, **extra_fields): Создает и
        сохраняет суперпользователя.
    Attributes:
        - use_in_migrations: Флаг, указывающий, что этот менеджер
        используется в миграциях.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с заданным email и паролем.
        param email и password: Email пользователя и Пароль пользователя.
        param extra_fields: Дополнительные поля пользователя.
        return: Созданный пользователь.
        """
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя.
        param email и password: Email пользователя и Пароль пользователя.ы
        param extra_fields: Дополнительные поля пользователя.
        return: Созданный пользователь.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя.
        param email и password: Email пользователя и Пароль пользователя.
        param extra_fields: Дополнительные поля суперпользователя.
        return: Созданный суперпользователь.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)