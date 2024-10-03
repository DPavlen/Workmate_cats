from django.contrib import admin

from .models import CustUser


@admin.register(CustUser)
class UsersAdmin(admin.ModelAdmin):
    """
    Администратор пользователей.
    """

    list_filter = ("email", "username")
    list_display = ("id", "role", "username", "email",)
    list_display_links = ("id", "username")
    search_fields = ("username", "role")
    empty_value_display = ("-пусто-",)