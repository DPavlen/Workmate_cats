from drf_spectacular.utils import (extend_schema, OpenApiParameter,
                                   OpenApiResponse)

custom_breeds_tags_schema = {"tags": ["breeds (Работа с породами котов)"]}
custom_cat_tags_schema = {"tags": ["cats (Работа с породами котов)"]}


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


CUSTOM_CAT_SCHEMA = {
    "list": extend_schema(
        **custom_cat_tags_schema,
        summary="Получение списка всех котят "
        "(Доступно только владельцам котов/кошек или админу).",
        description="Получение списка всех котят",
    ),
    "create": extend_schema(
        **custom_cat_tags_schema,
        summary="Создание нового кота/кошки. (Доступно любому "
        "пользователю).",
        description=(
            "Создание нового кота/кошки. При успешном создании кота/кошки, "
            "текущий пользователь присваивается как владелец."
        ),
        responses={
            201: OpenApiResponse(
                description="Кот/Кошка успешно создана."
            ),
        },
    ),
    "partial_update": extend_schema(
        **custom_cat_tags_schema,
        summary="Частичное обновление информации о коте/кошке. "
        "(Доступно только текущему пользователю или админу).",
        description="Частично обновляет информацию о коте/кошке.!"
        "При этом поля: 'Владелец кота/кошки', изменить нельзя! ",
    ),
    "destroy": extend_schema(
        **custom_cat_tags_schema,
        summary="Удаляет информацию от текущем коте/кошке (Доступно только текущему "
        "пользователю или админу).",
        description="Удаляет текущего кота/кошку (Доступно только текущему "
        "владельцу кота/кошки или админу).",
        responses={
            200: OpenApiResponse(
                description="Пользователь успешно удалён."
            ),
        },
    ),
    "retrieve": extend_schema(
        **custom_cat_tags_schema,
        summary="Получить информацию о кота/кошки по ID. (Доступно только "
        "текущему владельцу кота/кошки или админу).",
        description="Получить информацию о кота/кошки по ID. Возвращает "
        "информацию о конкретном запрошенном коте/кошке!",
    ),
    "photo": extend_schema(
        **custom_cat_tags_schema,
        summary="Добавляет фото к записи кота/кошки по ID кота/кошки. (Доступно только "
        "текущему владельцу кота/кошки или админу).",
        description="Добавляет фото к записи кота/кошки по ID кота/кошки. "
        "(Доступно только текущему владельцу кота/кошки или админу).",
    ),
}
