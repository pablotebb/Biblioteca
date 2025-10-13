from django.test import TestCase
from django.urls import reverse, resolve
from libros import views


class HomeViewTest(TestCase):
    """Pruebas para la vista home de la app libros."""

    def test_home_url_resolves_to_home_view(self):
        resolver = resolve("/libros/")
        self.assertEqual(resolver.func, views.home)

    def test_home_url_name_reverse_resolves_correctly(self):
        url = reverse("libros:Home")
        self.assertEqual(url, "/libros/")

    def test_home_view_returns_200(self):
        response = self.client.get(reverse("libros:Home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse("libros:Home"))
        self.assertTemplateUsed(response, "libros/home.html")


class HomeSecurityTest(TestCase):
    """Pruebas de seguridad para la vista home."""

    def setUp(self):
        self.response = self.client.get(reverse("libros:Home"))

    def test_security_headers_present(self):
        response = self.response
        self.assertEqual(response.get("X-Content-Type-Options"), "nosniff")
        self.assertIn(response.get("X-Frame-Options"), ["DENY", "SAMEORIGIN"])

    def test_no_sensitive_data_in_response(self):
        content = self.response.content.decode()
        self.assertNotIn("SECRET_KEY", content)
        self.assertNotIn("DEBUG =", content)
        self.assertNotIn("settings", content.lower())