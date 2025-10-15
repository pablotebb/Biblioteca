from django.test import TestCase
from django.urls import reverse, resolve
from core import views  # Asegúrate de reemplazar "myapp" con el nombre real de tu app

# Create your tests here.
class HomeViewTest(TestCase):
    """Pruebas para la vista home."""

    def test_home_url_resolves_to_home_view(self):
        """Verifica que la URL raíz resuelve a la vista home."""
        resolver = resolve("/")
        self.assertEqual(resolver.func, views.home)

    def test_home_url_name_reverse_resolves_correctly(self):
        """Verifica que el nombre 'Home' genera la URL correcta."""
        url = reverse("core:Home")
        self.assertEqual(url, "/")

    def test_home_view_returns_200(self):
        """Verifica que la vista home devuelve un código de estado 200."""
        response = self.client.get(reverse("core:Home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """
        Verifica que la vista home usa la plantilla correcta.
        Solo aplica si tu vista renderiza una plantilla.
        """
        response = self.client.get(reverse("core:Home"))
        #self.assertTemplateUsed(response, "home.html")  # Ajusta el nombre si usas otra
        self.assertTemplateUsed(response, "core/home.html")


class HomeSecurityTest(TestCase):
    """Pruebas de seguridad para la vista home."""

    def setUp(self):
        self.response = self.client.get(reverse("core:Home"))

    def test_security_headers_present(self):
        """Verifica que se envían cabeceras de seguridad activas por defecto."""
        response = self.response

        # 1. Protección contra MIME sniffing → SIEMPRE presente si SecurityMiddleware está activo
        self.assertEqual(response.get("X-Content-Type-Options"), "nosniff")

        # 2. Protección contra clickjacking → depende de X_FRAME_OPTIONS en settings.py
        self.assertIn(response.get("X-Frame-Options"), ["DENY", "SAMEORIGIN"])

        # NOTA: X-XSS-Protection ya NO se envía en Django moderno → no la pruebes

    def test_no_sensitive_data_in_response(self):
        """Asegura que no se filtran datos sensibles."""
        content = self.response.content.decode()
        self.assertNotIn("SECRET_KEY", content)
        self.assertNotIn("DEBUG =", content)
        self.assertNotIn("settings", content.lower())


class NavbarLinksTest(TestCase):
    """Pruebas del navbar común en la plantilla base."""

    def test_navbar_links_present_in_core_home(self):
        response = self.client.get(reverse("core:Home"))
        self.assertContains(response, f'href="{reverse("core:Home")}"')
        self.assertContains(response, f'href="{reverse("listado:Home")}"')
        self.assertContains(response, f'href="{reverse("libros:Home")}"')
        self.assertContains(response, f'href="{reverse("critica:Home")}"')

    def test_optional_security_headers_if_present(self):
        response = self.client.get(reverse("core:Home"))
        csp = response.get("Content-Security-Policy")
        if csp is not None:
            self.assertTrue(len(csp) > 0)
        referrer = response.get("Referrer-Policy")
        if referrer is not None:
            self.assertIn(referrer, [
                "no-referrer",
                "no-referrer-when-downgrade",
                "same-origin",
                "origin",
                "strict-origin",
                "origin-when-cross-origin",
                "strict-origin-when-cross-origin",
                "unsafe-url",
            ])
        permissions = response.get("Permissions-Policy")
        if permissions is not None:
            self.assertTrue(len(permissions) > 0)