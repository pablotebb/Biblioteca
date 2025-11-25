from django.test import TestCase
from django.urls import reverse, resolve
from libros import views
from django.contrib.auth.models import User
from libros.models import Libro, Categoria
from libros.forms import Formulario_libros


class LibroViewTest(TestCase):
    """Pruebas para la vista principal de libros."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.categoria = Categoria.objects.create(nombre='Ficción')
        self.libro = Libro.objects.create(
            id_libros=self.user,
            isbn='123456789',
            autor='Autor Test',
            titulo='Libro Test',
            contenido='Contenido de prueba'
        )
        self.libro.categoria.add(self.categoria)

    def test_libro_url_resolves_to_libro_view(self):
        resolver = resolve("/libros/")
        self.assertEqual(resolver.func, views.libro_view)

    def test_libro_url_name_reverse_resolves_correctly(self):
        url = reverse("libro:libros")
        self.assertEqual(url, "/libros/")

    def test_libro_view_returns_200(self):
        response = self.client.get(reverse("libro:libros"))
        self.assertEqual(response.status_code, 200)

    def test_libro_view_uses_correct_template(self):
        response = self.client.get(reverse("libro:libros"))
        self.assertTemplateUsed(response, "libros/libro.html")

    def test_form_is_present_in_template(self):
        response = self.client.get(reverse("libro:libros"))
        self.assertContains(response, "<form", html=False)
        self.assertContains(response, "csrfmiddlewaretoken", html=False)

    def test_libros_are_displayed_in_template(self):
        response = self.client.get(reverse("libro:libros"))
        self.assertContains(response, self.libro.titulo)
        self.assertContains(response, self.libro.autor)

    def test_post_creates_new_libro_when_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'isbn': '987654321',
            'autor': 'Nuevo Autor',
            'titulo': 'Nuevo Libro',
            'contenido': 'Nuevo contenido',
            'categoria': [self.categoria.id]
        }
        response = self.client.post(reverse("libro:libros"), data)
        self.assertEqual(response.status_code, 302)  # Redirect después de crear
        self.assertTrue(Libro.objects.filter(titulo='Nuevo Libro').exists())

    def test_post_redirects_when_form_invalid(self):
        self.client.login(username='testuser', password='testpass123')
        data = {}
        response = self.client.post(reverse("libro:libros"), data)
        self.assertEqual(response.status_code, 302)  # Redirect cuando hay errores


class EditarLibroViewTest(TestCase):
    """Pruebas para la vista de editar libro."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.categoria = Categoria.objects.create(nombre='Ficción')
        self.libro = Libro.objects.create(
            id_libros=self.user,
            isbn='123456789',
            autor='Autor Test',
            titulo='Libro Test',
            contenido='Contenido de prueba'
        )
        self.libro.categoria.add(self.categoria)

    def test_editar_libro_url_resolves_correctly(self):
        resolver = resolve(f"/libros/editar/{self.libro.pk}/")
        self.assertEqual(resolver.func, views.editar_libro)

    def test_editar_libro_url_name_reverse_resolves_correctly(self):
        url = reverse("libro:editar_libro", args=[self.libro.pk])
        self.assertEqual(url, f"/libros/editar/{self.libro.pk}/")

    def test_editar_libro_get_returns_200(self):
        response = self.client.get(reverse("libro:editar_libro", args=[self.libro.pk]))
        self.assertEqual(response.status_code, 200)

    def test_editar_libro_uses_correct_template(self):
        response = self.client.get(reverse("libro:editar_libro", args=[self.libro.pk]))
        self.assertTemplateUsed(response, "libros/formulario.html")

    def test_editar_libro_post_updates_book_when_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'isbn': '987654321',
            'autor': 'Autor Actualizado',
            'titulo': 'Título Actualizado',
            'contenido': 'Contenido actualizado',
            'categoria': [self.categoria.id]
        }
        response = self.client.post(reverse("libro:editar_libro", args=[self.libro.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.titulo, 'Título Actualizado')
        self.assertEqual(self.libro.autor, 'Autor Actualizado')

    def test_editar_libro_404_for_nonexistent_book(self):
        response = self.client.get(reverse("libro:editar_libro", args=[9999]))
        self.assertEqual(response.status_code, 404)


class BorrarLibroViewTest(TestCase):
    """Pruebas para la vista de borrar libro."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.categoria = Categoria.objects.create(nombre='Ficción')
        self.libro = Libro.objects.create(
            id_libros=self.user,
            isbn='123456789',
            autor='Autor Test',
            titulo='Libro Test',
            contenido='Contenido de prueba'
        )
        self.libro.categoria.add(self.categoria)

    def test_borrar_libro_url_resolves_correctly(self):
        resolver = resolve(f"/libros/borrar/{self.libro.pk}/")
        self.assertEqual(resolver.func, views.borrar_libro)

    def test_borrar_libro_url_name_reverse_resolves_correctly(self):
        url = reverse("libro:borrar_libro", args=[self.libro.pk])
        self.assertEqual(url, f"/libros/borrar/{self.libro.pk}/")

    def test_borrar_libro_get_returns_200(self):
        response = self.client.get(reverse("libro:borrar_libro", args=[self.libro.pk]))
        self.assertEqual(response.status_code, 200)

    def test_borrar_libro_uses_correct_template(self):
        response = self.client.get(reverse("libro:borrar_libro", args=[self.libro.pk]))
        self.assertTemplateUsed(response, "libros/confirmar_borrar.html")

    def test_borrar_libro_post_deletes_book(self):
        libro_id = self.libro.id
        response = self.client.post(reverse("libro:borrar_libro", args=[self.libro.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Libro.objects.filter(id=libro_id).exists())

    def test_borrar_libro_404_for_nonexistent_book(self):
        response = self.client.get(reverse("libro:borrar_libro", args=[9999]))
        self.assertEqual(response.status_code, 404)


class FormularioLibrosTest(TestCase):
    """Pruebas para el formulario de libros."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.categoria = Categoria.objects.create(nombre='Ficción')

    def test_formulario_valid_data(self):
        form_data = {
            'isbn': '123456789',
            'autor': 'Autor Test',
            'titulo': 'Libro Test',
            'contenido': 'Contenido de prueba',
            'categoria': [self.categoria.id]
        }
        form = Formulario_libros(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_missing_required_fields(self):
        form = Formulario_libros(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('isbn', form.errors)
        self.assertIn('autor', form.errors)
        self.assertIn('titulo', form.errors)
        self.assertIn('contenido', form.errors)

    def test_formulario_excludes_id_libros(self):
        form = Formulario_libros()
        self.assertNotIn('id_libros', form.fields)

    def test_formulario_widgets_have_correct_classes(self):
        form = Formulario_libros()
        self.assertEqual(form.fields['isbn'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['titulo'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['autor'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['contenido'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['categoria'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['imagen'].widget.attrs['class'], 'form-control')


class ModelTest(TestCase):
    """Pruebas para los modelos."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.categoria = Categoria.objects.create(nombre='Ficción')

    def test_categoria_str_representation(self):
        self.assertEqual(str(self.categoria), 'Ficción')

    def test_libro_str_representation(self):
        libro = Libro.objects.create(
            id_libros=self.user,
            isbn='123456789',
            autor='Autor Test',
            titulo='Libro Test',
            contenido='Contenido de prueba'
        )
        self.assertEqual(str(libro), 'Libro Test')

    def test_libro_creation_with_categoria(self):
        libro = Libro.objects.create(
            id_libros=self.user,
            isbn='123456789',
            autor='Autor Test',
            titulo='Libro Test',
            contenido='Contenido de prueba'
        )
        libro.categoria.add(self.categoria)
        self.assertEqual(libro.categoria.count(), 1)
        self.assertEqual(libro.categoria.first(), self.categoria)

    def test_categoria_verbose_names(self):
        self.assertEqual(Categoria._meta.verbose_name, 'categoria')
        self.assertEqual(Categoria._meta.verbose_name_plural, 'categorias')

    def test_libro_verbose_names(self):
        self.assertEqual(Libro._meta.verbose_name, 'libro')
        self.assertEqual(Libro._meta.verbose_name_plural, 'libros')
