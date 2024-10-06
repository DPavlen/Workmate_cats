from drf_spectacular.utils import (extend_schema, OpenApiParameter,
                                   OpenApiResponse)


auth_tags_schema = {"tags": ["auth (Операции с JWT-токенами. Авторизация пользователей)"]}
custom_users_tags_schema = {"tags": ["users (Работа с пользователями)"]}


CUSTOM_USERS_SCHEMA = {
    "list": extend_schema(
        **custom_users_tags_schema,
        summary="Получить список всех пользователей "
        " (Доступно авторизованному пользователю или админу).",
        description="Получить список всех пользователей",
    ),
    "create": extend_schema(
        **custom_users_tags_schema,
        summary="РЕГИСТРАЦИЯ. Создание нового пользователя (Доступно любому "
        "пользователю).",
        description=(
            "Создать нового пользователя. При успешном создании пользователя, "
            "он будет доступен для использования."
        ),
        responses={
            201: OpenApiResponse(
                description="Пользователь успешно создан."
            ),
        },
    ),
    "partial_update": extend_schema(
        **custom_users_tags_schema,
        summary="ПРОФИЛЬ. Частичное обновление информации о пользователе. "
        "(Доступно только текущему пользователю или админу).",
        description="Частично обновляет информацию о пользователе!"
        "При этом поля: 'Логин пользователя', 'Адрес электронной "
        "почты' изменить нельзя! ",
    ),
    "update": extend_schema(
        **custom_users_tags_schema,
        summary="Обновить информацию о пользователе полностью.  "
        "(Доступно только текущему пользователю или админу).",
        description="Обновляет данные информацию о пользователе. "
        "При этом поля: 'Логин пользователя', 'Адрес электронной "
        "почты' изменить нельзя! ",
    ),
    "destroy": extend_schema(
        **custom_users_tags_schema,
        summary="Удаляет текущего пользователя (Доступно только текущему "
        "пользователю или админу).",
        description="Удаляет текущего пользователя (Доступно только текущему "
        "пользователю или админу).",
        responses={
            200: OpenApiResponse(
                description="Пользователь успешно удалён."
            ),
        },
    ),
    "retrieve": extend_schema(
        **custom_users_tags_schema,
        summary="Получить информацию о пользователе по ID. (Доступно только "
        "текущему пользователю или админу).",
        description="Получить информацию о пользователе по ID. Возвращает "
        "информацию о конкретном запрошенном пользователе!",
    ),
}


JWT_CREATE_SCHEMA = extend_schema(
    **auth_tags_schema,
    summary="Создание JWT-токена (Доступно: Кто прошел регистрацию.)",
    description="Для создания JWT-токена, необходимо указать: email и пароль!",
    responses={
            200: OpenApiResponse(
                description="JWT-токены access и refresh созданы."
            ),
        },
)

JWT_TOKEN_REFRESH_SCHEMA = extend_schema(
    **auth_tags_schema,
    summary="Обновление JWT-токена (Доступно: У кого уже создан токен.)",
    description="Для обновления JWT-токена, вводим в поле: 'refresh': "
    "'refresh_token', "
    "который мы получаем с эндпойнта api/auth/jwt/create/ ",
)

JWT_TOKEN_VERIFY_SCHEMA = extend_schema(
    **auth_tags_schema,
    summary="Проверка(верификация) JWT-токена (Доступно: У кого уже создан "
    "токен.)",
    description="Для проверки(верификации) JWT-токена, вводим в поле: "
    "'token': 'access_token' , который мы получаем "
    "с эндпойнта api/auth/jwt/create/  ",
)
