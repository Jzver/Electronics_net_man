from rest_framework import serializers

from electronics.models import NetworkObject, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class NetworkObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkObject
        exclude = ("products",)


class NetworkObjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkObject
        fields = ("name", "country", "town", "street", "house", "phone_number", "provider", "email")


class NetworkObjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkObject
        fields = ("name", "country", "town", "street", "house", "phone_number", "provider", "email", "debt_to_provider")


class NetworkObjectDetailSerializer(serializers.ModelSerializer):
    count_products_for_networkobject = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)
    url_provider = serializers.SerializerMethodField()
    hierarchy = serializers.SerializerMethodField()

    @staticmethod
    def get_count_products_for_networkobject(networkobject):
        return networkobject.products.count()

    @staticmethod
    def get_url_provider(networkobject):
        provider = networkobject.provider
        url_provider = f"http://127.0.0.1:8000/network/networkobjects/{provider.pk}/"
        return url_provider

    @staticmethod
    def get_hierarchy(networkobject):
        if "Завод" in networkobject.name:
            hierarchy = 0
        elif networkobject.pk == networkobject.provider.pk:
            hierarchy = 0
        else:
            hierarchy = 1
        return hierarchy

    class Meta:
        model = NetworkObject
        fields = "__all__"