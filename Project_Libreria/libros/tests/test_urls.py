from django.test import TestCase
from django.urls import reverse, resolve
from ..views import libro_view, editar_libro, borrar_libro
from ..models import Libro, User, Categoria

class UrlsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.categoria = Categoria.objects.create(nombre='Aventura')
        self.libro = Libro.objects.create(
            id_libros=self.user,
            isbn='123-4567890123',
            autor='Autor de Prueba',
            titulo='Libro de Prueba',
            contenido='Contenido de prueba.'
        )
        self.libro.categoria.add(self.categoria)

    def test_libros_url_is_resolved(self):
        url = reverse('libro:libros')
        self.assertEqual(resolve(url).func, libro_view)

    def test_editar_libro_url_is_resolved(self):
        url = reverse('libro:editar_libro', args=[self.libro.pk])
        self.assertEqual(resolve(url).func, editar_libro)
        
    def test_borrar_libro_url_is_resolved(self):
        url = reverse('libro:borrar_libro', args=[self.libro.pk])
        self.assertEqual(resolve(url).func, borrar_libro)
