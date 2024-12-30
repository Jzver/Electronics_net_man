from django.test import TestCase, Client
from django.urls import reverse
from electronics.models import Product, NetworkObject


class ProductModelTests(TestCase):
    def setUp(self):
        Product.objects.create(
            name="Test Product",
            model="Test Model",
            launch_date="2022-01-01",
            description="This is a test product.",
        )

    def test_product_creation(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.model, "Test Model")
        self.assertEqual(product.launch_date, "2022-01-01")
        self.assertEqual(product.description, "This is a test product.")

    def test_product_str(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(str(product), "Test Product")


class NetworkObjectModelTests(TestCase):
    def setUp(self):
        NetworkObject.objects.create(
            name="Test Network Object",
            country="Test Country",
            town="Test Town",
            street="Test Street",
            house=123,
            phone_number="1234567890",
            email="test@example.com",
            provider=None,
            debt_to_provider=0.00,
        )

    def test_networkobject_creation(self):
        network_object = NetworkObject.objects.get(name="Test Network Object")
        self.assertEqual(network_object.name, "Test Network Object")
        self.assertEqual(network_object.country, "Test Country")
        self.assertEqual(network_object.town, "Test Town")
        self.assertEqual(network_object.street, "Test Street")
        self.assertEqual(network_object.house, 123)
        self.assertEqual(network_object.phone_number, "1234567890")
        self.assertEqual(network_object.email, "test@example.com")
        self.assertIsNone(network_object.provider)
        self.assertEqual(network_object.debt_to_provider, 0.00)

    def test_networkobject_str(self):
        network_object = NetworkObject.objects.get(name="Test Network Object")
        self.assertEqual(str(network_object), "Test Network Object")

    def test_networkobject_get_full_address(self):
        network_object = NetworkObject.objects.get(name="Test Network Object")
        self.assertEqual(network_object.get_full_address(), "Test Street, 123, Test Town, Test Country")

    def test_networkobject_check_debt(self):
        network_object = NetworkObject.objects.get(name="Test Network Object")
        self.assertFalse(network_object.check_debt())

    def test_networkobject_debt_status(self):
        network_object = NetworkObject.objects.get(name="Test Network Object")
        self.assertEqual(network_object.debt_status, "Долг в пределах допустимого лимита")


class NetworkObjectAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_url = reverse("admin:index")
        self.login_url = reverse("admin:login")
        self.networkobject_url = reverse("admin:electronics_networkobject_changelist")

    def test_login(self):
        response = self.client.post(self.login_url, {"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(self.admin_url)

    def test_list_networkobjects(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.networkobject_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("admin/networkobject/change_list.html")

    def test_change_networkobject(self):
        self.client.login(username="testuser", password="testpassword")
        network_object = NetworkObject.objects.create(name="Test Network Object", country="Test Country")
        response = self.client.get(f"{self.networkobject_url}{network_object.pk}/change/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("admin/networkobject/change_form.html")

    def test_delete_networkobject(self):
        self.client.login(username="testuser", password="testpassword")
        network_object = NetworkObject.objects.create(name="Test Network Object", country="Test Country")
        response = self.client.post(f"{self.networkobject_url}{network_object.pk}/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(self.networkobject_url)
        self.assertFalse(NetworkObject.objects.filter(pk=network_object.pk).exists())

    def test_change_password(self):
        self.client.login(username="admin@gmail.com", password="22092013")
        response = self.client.post(reverse("admin:password_change"),
                                    {"password1": "newpassword", "password2": "newpassword"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(self.admin_url)
        self.assertTrue(self.client.login(username="admin@gmail.com", password="newpassword"))