from django_filters import rest_framework as filters

from .models import Breed


class FilterBreed(filters.FilterSet):
    """
    Фильтрация по определенной породе котов и кошек.
    """

    name = filters.CharFilter(
        field_name="name",
        lookup_expr="istartswith",
        label="Название породы котов",
        help_text="Введите название породы котов, например 'Си', "
                  "получим: Сингапурская и Сиамская."
    )

    class Meta:
        model = Breed
        fields = (
            "name",
        )