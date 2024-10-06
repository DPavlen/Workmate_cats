from drf_spectacular.utils import (extend_schema, OpenApiResponse)

custom_breeds_tags_schema = {"tags": ["breeds (Работа с породами котов)"]}
custom_cat_tags_schema = {"tags": ["cats (Работа с породами котов)"]}
custom_cat_rating_tags_schema = {"tags": ["cats-ratings (Работа с рейтингом и оценками)"]}


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


CUSTOM_CAT_RATING_SCHEMA = {
    "list": extend_schema(
        **custom_cat_rating_tags_schema,
        summary="Получение списка оценок котов. (Доступно только владельцам котов/кошек или админу).",
        description="Получение списка оценок всех котов."
    ),
    "create": extend_schema(
        **custom_cat_rating_tags_schema,
        summary="Создание новой оценки кота. (Доступно аутентифицированому пользователю).",
        description=(
            "Создание новой оценки для кота. При успешном создании оценки, "
            "текущий пользователь автоматически назначается как автор."
        ),
        responses={
            201: OpenApiResponse(
                description="Оценка кота успешно создана."
            ),
        },
    ),
    "destroy": extend_schema(
        **custom_cat_rating_tags_schema,
        summary="Удаление оценки кота. (Доступно только текущему пользователю или админу).",
        description="Удаляет оценку кота (Доступно только текущему автору оценки или админу).",
        responses={
            200: OpenApiResponse(
                description="Оценка успешно удалена."
            ),
        },
    ),
    "get_highest_rated_cats": extend_schema(
        **custom_cat_rating_tags_schema,
        summary="Коты, отсортированные по средней оценке(по убыванию). (Доступно всем пользователям).",
        description="Коты, отсортированные по средней оценке(по убыванию). Коты без оценок не выводятся сюда. "
                    " (Доступно всем пользователям).",
        responses={
            200: OpenApiResponse(
                description="Оценка успешно удалена."
            ),
        },
    ),
}