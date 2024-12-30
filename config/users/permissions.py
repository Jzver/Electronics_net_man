from rest_framework import permissions


class IsActiveAndIsStaff(permissions.BasePermission):
    """
    Класс для проверки является ли Пользователь Активным (is_active) Сотрудником (is_staff)
    """

    message = "Вы не являетесь активным сотрудником или данное поле нельзя изменить"

    def has_permission(self, request, view):
        """
        Метод проверки на то, что пользователь is_active и is_staff.
        """
        return request.user.is_active and request.user.is_staff