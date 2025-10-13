from django.test import TestCase
from django.urls import reverse


class ProjectUrlIntegrationTest(TestCase):
    """Pruebas de integración para las URLs principales del proyecto."""

    def test_core_home_resolves_and_returns_200(self):
        """La URL raíz (/) debe devolver 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_critica_namespace_resolves(self):
        """Verifica que la URL de crítica está accesible (aunque redirija o muestre lista)."""
        # Asumimos que critica tiene una vista en su raíz, ej. lista de críticas
        response = self.client.get("/critica/")
        # Puede ser 200 (pública) o 302 (requiere login), pero NO debe ser 404
        self.assertNotEqual(response.status_code, 404)

    def test_libros_namespace_resolves(self):
        """Verifica que /libros está accesible."""
        response = self.client.get("/libros/")
        self.assertNotEqual(response.status_code, 404)

    def test_listado_namespace_resolves(self):
        """Verifica que /listado/ está accesible."""
        response = self.client.get("/listado/")
        self.assertNotEqual(response.status_code, 404)

    def test_admin_url_resolves(self):
        """La URL de admin debe existir (aunque redirija al login)."""
        response = self.client.get("/admin/")
        # En producción, sin login, suele ser 302 (redirección a login)
        self.assertIn(response.status_code, [200, 302])  # 200 si DEBUG=True y ya logueado


class ProjectSecurityHeadersTest(TestCase):
    """Pruebas de seguridad HTTP en rutas públicas del proyecto."""

    def _check_security_headers(self, response):
        """Verifica cabeceras de seguridad comunes."""
        self.assertEqual(response.get("X-Content-Type-Options"), "nosniff")
        self.assertIn(response.get("X-Frame-Options"), ["DENY", "SAMEORIGIN"])

    def test_core_home_has_security_headers(self):
        response = self.client.get("/")
        self._check_security_headers(response)

    def test_critica_has_security_headers(self):
        response = self.client.get("/critica/")
        if response.status_code != 404:
            self._check_security_headers(response)

    def test_libros_has_security_headers(self):
        response = self.client.get("/libros/")
        if response.status_code != 404:
            self._check_security_headers(response)

    def test_listado_has_security_headers(self):
        response = self.client.get("/listado/")
        if response.status_code != 404:
            self._check_security_headers(response)