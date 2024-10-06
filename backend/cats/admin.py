from django.contrib import admin
from django.utils.html import format_html

from .models import Group, Breed, Cat, CatPhoto, CatRating


class BaseAdminSettings(admin.ModelAdmin):
    """Базовые настройки для всех моделей."""
    list_display = ("id", "name", "created")
    list_display_links = ("id", "name")
    search_fields = ("id", "name", "created")
    empty_value_display = "-пусто-"


class GroupBreedInline(admin.TabularInline):
    """
    Связь между группой и породой кота в административной панели.
    """
    model = Breed
    min_num = 0
    extra = 0


@admin.register(Group)
class GroupAdmin(BaseAdminSettings):
    """Административный интерфейс для управления группами котов."""
    inlines = [GroupBreedInline]


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления породами котов."""
    list_display = BaseAdminSettings.list_display + ("group",)
    list_display_links = BaseAdminSettings.list_display_links + ("group",)
    search_fields = BaseAdminSettings.search_fields + ("group",)


@admin.register(CatPhoto)
class CatPhotoAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления фото котов."""
    list_display = (
        "id",
        "cat",
        "photo",
    )
    search_fields = ("cat", "photo")


class CatPhotoInline(admin.TabularInline):
    """Связь между фото и котом в административной панели."""
    model = CatPhoto
    extra = 1


@admin.register(Cat)
class CatAdmin(BaseAdminSettings):
    """Административный интерфейс для управления породами котов."""
    list_display = BaseAdminSettings.list_display + (
        "breed", "color", "age", "sex", "owner")
    list_display_links = BaseAdminSettings.list_display_links + (
        "breed", "color", "age", "sex", "owner")
    search_fields = BaseAdminSettings.search_fields + (
        "breed", "color", "age", "sex", "owner")
    inlines = (CatPhotoInline,)


@admin.register(CatRating)
class CatRatingAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления породами котов."""
    list_display = ("id", "cat", "user", "rating")
    list_filter = ("id", "cat", "rating")
    search_fields = ("id", "cat__name", "user__username")
    ordering = ("id", "cat", "user")

    fieldsets = (
        (None, {
            "fields": ("cat", "user", "rating")
        }),
    )
