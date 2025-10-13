from django.test import TestCase
from django.urls import reverse, resolve
from listado import views


class HomeViewTest(TestCase):
    """Pruebas para la vista home de la app listado."""

    def test_home_url_resolves_to_home_view(self):
        resolver = resolve("/listado/")
        self.assertEqual(resolver.func, views.home)

    def test_home_url_name_reverse_resolves_correctly(self):
        url = reverse("listado:Home")
        self.assertEqual(url, "/listado/")

    def test_home_view_returns_200(self):
        response = self.client.get(reverse("listado:Home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse("listado:Home"))
        self.assertTemplateUsed(response, "listado/home.html")


class HomeSecurityTest(TestCase):
    """Pruebas de seguridad para la vista home."""

    def setUp(self):
        self.response = self.client.get(reverse("listado:Home"))

    def test_security_headers_present(self):
        response = self.response
        self.assertEqual(response.get("X-Content-Type-Options"), "nosniff")
        self.assertIn(response.get("X-Frame-Options"), ["DENY", "SAMEORIGIN"])

    def test_no_sensitive_data_in_response(self):
        content = self.response.content.decode()
        self.assertNotIn("SECRET_KEY", content)
        self.assertNotIn("DEBUG =", content)
        self.assertNotIn("settings", content.lower())