from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from users.models import CustUser
from users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """
    Кастомный ViewSet для работы с пользователями.
    Предоставляет эндпоинты для управления пользователями, включая активацию.
    """

    queryset = CustUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
        """
        if self.action == "list":
            return (IsAdminUser(),)
        return (AllowAny(),)