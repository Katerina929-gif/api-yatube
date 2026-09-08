from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """

    Разрешает изменение контента только его автору.

    Для остальных авторизованных пользователей — доступ только на чтение.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет права доступа к конкретному объекту.

        Разрешает безопасные методы (GET, HEAD, OPTIONS) для всех залогиненных
        пользователей. Методы изменения данных (PUT, PATCH, DELETE)
        разрешены только автору объекта.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
