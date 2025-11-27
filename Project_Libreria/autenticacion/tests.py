from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AutenticacionViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("autenticacion")
        self.login_url = reverse("logear")
        self.logout_url = reverse("cerrar_sesion")
        self.home_url = reverse("core:Home")  # Assuming "Home" is a valid URL name in your project

        # Create a test user
        self.test_user = User.objects.create_user(username="testuser", password="testpassword")

    def test_registro_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registro/registro.html")

    def test_registro_view_post_success(self):
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "password": "casimiro78&",
            "password2": "casimiro78&",
        })
        # It should redirect to Home after successful registration
        self.assertRedirects(response, self.home_url)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_registro_view_post_invalid(self):
        response = self.client.post(self.register_url, {
            "username": "testuser",  # User already exists
            "password": "casimiro78&",
            "password2": "casimiro78&",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registro/registro.html")
        self.assertContains(response, "Ya existe un usuario con este nombre.")

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/login.html")

    def test_login_view_post_success(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword",
        })
        self.assertRedirects(response, self.home_url)
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "wrongpassword",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/login.html")
        self.assertContains(response, "Por favor, introduzca un nombre de usuario y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas.")
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)
