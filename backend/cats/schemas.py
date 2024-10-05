from drf_spectacular.utils import (extend_schema, OpenApiParameter,
                                   OpenApiResponse)

custom_breeds_tags_schema = {"tags": ["breeds (Работа с породами котов)"]}


CUSTOM_BREEDS_SCHEMA = {
    "list": extend_schema(
        **custom_breeds_tags_schema,
        summary=" Получить список всех пород котов "
        " (Доступно всем: Не требует аутентификации).",
        description="/api/breeds/ Получить список всех пород котов",
    ),
    "retrieve": extend_schema(
        **custom_breeds_tags_schema,
        summary="Получить информацию о породе кота по ID. "
                "(Доступно всем: Не требует аутентификации).",
        description="/api/breeds/{id} Получить информацию о породе кота по ID. Возвращает "
        "информацию о конкретной запрошенной породе кота!",
    ),
}