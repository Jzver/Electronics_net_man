from django.db import models

class Product(models.Model):
    """
    Класс модели продукта.
    """

    name = models.CharField(
        max_length=150,
        verbose_name="Название продукта",
        help_text="Введите название продукта",
    )
    model = models.CharField(
        max_length=150,
        verbose_name="Модель продукта",
        help_text="Введите модель продукта",
        blank=True,
        null=True,
    )
    launch_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата выхода продукта на рынок",
        help_text="Введите дату выхода продукта на рынок",
    )
    description = models.TextField(
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]  # Добавлено для сортировки по названию продукта

    def __str__(self):
        return self.name

class NetworkObject(models.Model):
    """
    Класс модели объекта сети.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Название объекта сети",
        help_text="Введите название объекта сети",
    )
    email = models.EmailField(
        verbose_name="Email",
        help_text="Введите email",
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        help_text="Введите название страны",
        blank=True,
        null=True,
    )
    town = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Введите название города",
        blank=True,
        null=True,
    )
    street = models.CharField(
        max_length=100,
        verbose_name="Улица",
        help_text="Введите название улицы",
        blank=True,
        null=True,
    )
    house = models.PositiveIntegerField(
        verbose_name="Номер дома",
        help_text="Введите номер дома",
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        blank=True,
        null=True,
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
    )
    provider = models.ForeignKey(
        "self",  # Исправлено на ссылку на саму модель NetworkObject
        verbose_name="Поставщик",
        on_delete=models.CASCADE,
        help_text="Укажите поставщика",
        blank=True,
        null=True,
    )
    debt_to_provider = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Долг перед поставщиком",
        help_text="Введите долг перед поставщиком",
        blank=True,
        null=True,
    )
    time_of_creation = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    MAX_DEBT = 10000  # Максимально допустимый долг перед поставщиком

    def get_full_address(self):
        return f"{self.street}, {self.house}, {self.town}, {self.country}"

    class Meta:
        ordering = ["town"]  # Добавлено для сортировки по городу
        verbose_name = "Объект сети"
        verbose_name_plural = "Объекты сети"

    def __str__(self):
        return self.name

    def check_debt(self):
        return self.debt_to_provider > self.MAX_DEBT

    @property
    def debt_status(self):
        if self.check_debt():
            return "Долг превышает допустимый лимит"
        else:
            return "Долг в пределах допустимого лимита"