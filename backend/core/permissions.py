from rest_framework import permissions


class IsOwnerOrReadOnlyOrAdmin(permissions.BasePermission):
    """
    Пользователь может редактировать только свои собственные объекты.
    """

    def has_permission(self, request, view):
        """
        Проверяем разрешения на уровне представлений(view)
        """

        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return False

        # Если запрос на чтение, разрешаем доступ
        if request.method in permissions.SAFE_METHODS:
            return True

        return True

    def has_object_permission(self, request, view, obj):
        """
        Проверяем разрешения на уровне объекта.
        """

        # Разрешить любые запросы на чтение.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить редактирование объекта только автору или админу.
        return (
            request.user.is_authenticated
            and (
                obj == request.user or
                request.user.is_staff or
                request.user.role == "admin")
        )