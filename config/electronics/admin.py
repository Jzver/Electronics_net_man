from django.contrib import admin
from django.utils.html import format_html
from electronics.models import NetworkObject, Product


# Создаем пользовательское действие для очистки долга перед поставщиком
@admin.action(description="Очистить долг перед поставщиком")
def clear_debt_to_provider(modeladmin, request, queryset):
    queryset.update(debt_to_provider=0.00)


# Регистрируем и настраиваем модель Product в административном интерфейсе
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Поля, которые отображаются в виде списка в административном интерфейсе
    list_display = ("id", "name", "model", "description")
    # Поля, по которым можно фильтровать в административном интерфейсе
    list_filter = ("name",)
    # Поля, по которым можно осуществлять поиск в административном интерфейсе
    search_fields = ("name__icontains", "description__icontains")
    # Поля, которые можно редактировать в режиме списка
    list_editable = ("model",)
    # Поля, которые можно редактировать в режиме редактирования
    readonly_fields = ("id",)
    # Группируем поля в разделах в режиме редактирования
    fieldsets = (
        ("Основная информация", {"fields": ("name", "model")}),
        ("Описание", {"fields": ("description",)}),
    )
    # Добавляем возможность сохранять объекты как черновики
    save_as = True


# Регистрируем и настраиваем модель NetworkObject в административном интерфейсе
@admin.register(NetworkObject)
class NetworkObjectAdmin(admin.ModelAdmin):
    # Поля, которые отображаются в виде списка в административном интерфейсе
    list_display = (
        "id",
        "name",
        "email",
        "country",
        "town",
        "street",
        "house",
        "phone_number",
        "provider",
        "debt_to_provider",
        "time_of_creation",
        "display_full_address",
        "debt_status",
        "display_products",
    )
    # Поля, по которым можно фильтровать в административном интерфейсе
    list_filter = ("name", "town", "provider")
    # Поля, по которым можно осуществлять поиск в административном интерфейсе
    search_fields = (
        "name__icontains", "country__icontains", "town__icontains", "street__icontains", "phone_number__icontains")
    # Поля, которые можно редактировать в режиме списка
    list_editable = ("email", "phone_number")
    # Поля, которые можно редактировать в режиме редактирования
    readonly_fields = ("id", "time_of_creation")
    # Группируем поля в разделах в режиме редактирования
    fieldsets = (
        ("Основная информация", {"fields": ("name", "email", "phone_number")}),
        ("Адрес", {"fields": ("country", "town", "street", "house")}),
        ("Долг перед поставщиком", {"fields": ("provider", "debt_to_provider")}),
    )
    # Добавляем возможность упрощенного выбора связанных продуктов в режиме редактирования
    filter_horizontal = ("products",)
    # Добавляем пользовательское действие для модели NetworkObject
    actions = [clear_debt_to_provider]

    # Переопределяем метод get_queryset для предзагрузки связанных продуктов и улучшения производительности
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("products")

    # Пользовательский метод для отображения полного адреса объекта сети в административном интерфейсе
    def display_full_address(self, obj):
        return f"{obj.street}, {obj.house}, {obj.town}, {obj.country}"

    display_full_address.short_description = "Полный адрес"

    # Пользовательский метод для отображения статуса долга объекта сети в административном интерфейсе
    def debt_status(self, obj):
        if obj.check_debt():
            return format_html('<span style="color: red;">Долг</span>')
        else:
            return format_html('<span style="color: green;">Нет долга</span>')

    debt_status.short_description = "Статус долга"
    debt_status.allow_tags = True

    # Пользовательский метод для отображения связанных продуктов объекта сети в административном интерфейсе
    def display_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])

    display_products.short_description = "Продукты"
