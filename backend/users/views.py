from djoser import utils
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from core.permissions import IsOwnerOrReadOnlyOrAdmin
from users.models import CustUser
from users.schemas import (
    JWT_CREATE_SCHEMA, JWT_TOKEN_REFRESH_SCHEMA,
    JWT_TOKEN_VERIFY_SCHEMA, CUSTOM_USERS_SCHEMA
)
from users.serializers import CustomUserSerializer, CustomUserUpdateSerializer, CustomUserReadSerializer


@extend_schema_view(**CUSTOM_USERS_SCHEMA)
class CustomUserViewSet(UserViewSet):
    """
     Кастомный ViewSet для работы с пользователями.
     Этот ViewSet предоставляет эндпоинты для управления пользователями,
     включая активацию и частичное обновление.
     Attributes:
     - queryset: Запрос, возвращающий все объекты User (CustUser).
     - serializer_class: Сериализатор, используемый для преобразования
     данных пользователя.
     - lookup_field: Имя поля в URL для поиска объекта (по умолчанию "pk"
     для UUID).
     Permissions:
         - permission_classes: Список классов разрешений для ViewSet.
    Methods:
    - list - Возвращает список всех пользователей.
     - create -  Создает нового пользователя.
     - retrieve - Возвращает информацию о конкретном пользователе.
     - update - Обновляет информацию о конкретном пользователе.
     - partial_update -  Частично обновляет информацию о конкретном
     пользователе.
     - destroy -  Удаляет конкретного пользователя.
    """

    lookup_field = "pk"

    def get_queryset(self):
        """
        Получение всех пользователей.
        """
        queryset = CustUser.objects.all()
        return queryset

    def get_serializer_class(self):
        """
        Выбор подходящего сериализатора на основе типа действия.
        """
        if self.action == "create":
            return CustomUserSerializer
        if self.action == "partial_update":
            return CustomUserUpdateSerializer
        return CustomUserReadSerializer

    def get_permissions(self):
        """
        Возвращает соответствующие разрешения в зависимости от действия.
        """

        action_permissions = {
            "list": (IsOwnerOrReadOnlyOrAdmin(),),
            "retrieve": (IsOwnerOrReadOnlyOrAdmin(),),
            "create": (AllowAny(),),
            "update": (IsOwnerOrReadOnlyOrAdmin(),),
            "partial_update": (IsOwnerOrReadOnlyOrAdmin(),),
            "destroy": (IsOwnerOrReadOnlyOrAdmin(),),
        }
        return action_permissions.get(self.action, super().get_permissions())

    def list(self, request, *args, **kwargs):
        """
        Возвращает список всех пользователей.
        """

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Создает нового пользователя.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Возвращает информацию о конкретном пользователе.
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Обновляет информацию о конкретном пользователе.
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет информацию о конкретном пользователе.
        """
        user = self.request.user
        if user.is_authenticated:
            serializer = self.get_serializer(
                user,
                data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save(id=user.id)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет конкретного пользователя.
        """
        instance = self.get_object()
        user_id = instance.id

        if instance == request.user:
            utils.logout_user(self.request)
        self.perform_destroy(instance)

        return Response(
            {"message": "Пользователь успешно удален", "id": user_id},
            status=status.HTTP_200_OK
        )


@JWT_CREATE_SCHEMA
class CustomTokenCreateView(TokenObtainPairView):
    """
    Кастомный viewset для создания JWT-токена.
    """

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@JWT_TOKEN_REFRESH_SCHEMA
class CustomTokenRefreshView(TokenRefreshView):
    """
    Viewset для обновления JWT-токена с помощью refresh_token.
    """

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@JWT_TOKEN_VERIFY_SCHEMA
class CustomTokenVerifyView(TokenVerifyView):
    """
    Viewset для проверки(верификации) JWT-токена c помощью access_token.
    """

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)