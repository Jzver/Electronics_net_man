from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """Класс для создания модели Пользователя"""

    username = None
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name="Электронная почта",
        help_text="Введите ваш email",
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        help_text="Введите ваше имя",
        error_messages={
            'required': 'Имя обязательно для заполнения.',
        },
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        help_text="Введите вашу фамилию",
        error_messages={
            'required': 'Фамилия обязательна для заполнения.',
        },
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        """метод для валидации данных перед сохранением сущности"""
        if not self.first_name or not self.last_name:
            raise ValidationError("Имя и фамилия обязательны для заполнения.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
