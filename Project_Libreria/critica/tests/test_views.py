from django.test import TestCase
from django.urls import reverse, resolve
from critica import views
from django.contrib.auth.models import User
from libros.models import Libro, Categoria
from critica.models import Critica


class HomeViewTest(TestCase):
    """Pruebas para la vista home de la app critica."""

    def setUp(self):
        """Crea un usuario y lo loguea para las pruebas de esta clase."""
        self.user = User.objects.create_user(username='hometestuser', password='password123')
        self.client.login(username='hometestuser', password='password123')

    def test_home_url_resolves_to_home_view(self):
        resolver = resolve(reverse("critica:critica"))
        self.assertEqual(resolver.func, views.critica_view)

    def test_home_url_name_reverse_resolves_correctly(self):
        url = reverse("critica:critica")
        self.assertEqual(url, "/critica/")

    def test_home_view_returns_200(self):
        response = self.client.get(reverse("critica:critica"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse("critica:critica"))
        self.assertTemplateUsed(response, "critica/critica.html")

    def test_form_is_present_in_template(self):
        response = self.client.get(reverse("critica:critica"))
        self.assertContains(response, "<form", html=False)
        self.assertContains(response, "csrfmiddlewaretoken", html=False)


class HomeSecurityTest(TestCase):
    """Pruebas de seguridad para la vista home."""

    def setUp(self):
        """Crea un usuario, lo loguea y obtiene la respuesta."""
        self.user = User.objects.create_user(username='securityuser', password='password123')
        self.client.login(username='securityuser', password='password123')
        self.response = self.client.get(reverse("critica:critica"))

    def test_security_headers_present(self):
        response = self.response
        self.assertEqual(response.get("X-Content-Type-Options"), "nosniff")
        self.assertIn(response.get("X-Frame-Options"), ["DENY", "SAMEORIGIN"])

    def test_no_sensitive_data_in_response(self):
        content = self.response.content.decode()
        self.assertNotIn("SECRET_KEY", content)
        self.assertNotIn("DEBUG =", content)
        self.assertNotIn("settings", content.lower())


class CriticaFormViewTest(TestCase):
    """Pruebas para el envío del formulario en la vista home."""

    @classmethod
    def setUpTestData(cls):
        """Crea datos necesarios para las pruebas de envío de formulario."""
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.categoria = Categoria.objects.create(nombre='Ensayo')
        # CORRECCIÓN: El campo 'id_libros' debe ser una instancia de User.
        libro = Libro.objects.create(
            titulo='Libro para criticar',
            autor='Autor',
            id_libros=cls.user
        )
        libro.categoria.set([cls.categoria])
        cls.libro = libro
        cls.url = reverse("critica:critica")

    def setUp(self):
        """Inicia sesión con el usuario de prueba antes de cada test."""
        self.client.login(username='testuser', password='password123')

    def test_post_valid_form_creates_critica_and_redirects(self):
        """Verifica que un POST válido crea una crítica y redirige."""
        form_data = {
            'libro': self.libro.id,
            'titulo': 'Crítica desde Test',
            'contenido': 'Contenido de la crítica.',
            'puntuacion': 5
        }
        response = self.client.post(self.url, data=form_data)
        
        # Verifica que se creó la crítica en la base de datos
        self.assertTrue(Critica.objects.filter(titulo='Crítica desde Test').exists())
        
        # Verifica que el usuario es redirigido (código 302)
        self.assertEqual(response.status_code, 302)
        # Asumiendo que redirige a la misma página o a una de éxito
        self.assertRedirects(response, self.url)

    def test_post_invalid_form_rerenders_page_with_errors(self):
        """Verifica que un POST inválido vuelve a mostrar el formulario con errores."""
        form_data = {'libro': self.libro.id, 'titulo': 'Título inválido'}  # Faltan campos
        response = self.client.post(self.url, data=form_data)
        
        self.assertEqual(response.status_code, 200)  # No redirige, muestra la página de nuevo
        self.assertFormError(response.context['form'], 'contenido', 'Este campo es obligatorio.')