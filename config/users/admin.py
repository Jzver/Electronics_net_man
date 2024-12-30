from django.contrib import admin

# Register your models here.
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для регистрации User в админке."""

    list_display = ("id", "email", "is_active", "password", "first_name", "second_name")
    list_filter = ("email",)
    search_fields = ("email",)