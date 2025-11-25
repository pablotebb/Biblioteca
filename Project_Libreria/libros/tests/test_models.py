from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Categoria, Libro

class CategoriaModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Categoria.objects.create(nombre='Test Categoria')

    def test_nombre_label(self):
        categoria = Categoria.objects.get(id=1)
        field_label = categoria._meta.get_field('nombre').verbose_name
        self.assertEqual(field_label, 'nombre')

    def test_nombre_max_length(self):
        categoria = Categoria.objects.get(id=1)
        max_length = categoria._meta.get_field('nombre').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_nombre(self):
        categoria = Categoria.objects.get(id=1)
        expected_object_name = f'{categoria.nombre}'
        self.assertEqual(expected_object_name, str(categoria))

class LibroModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='testuser', password='testpassword')
        categoria = Categoria.objects.create(nombre='Test Categoria')
        libro = Libro.objects.create(
            id_libros=user,
            isbn='1234567890',
            autor='Test Autor',
            titulo='Test Titulo',
            contenido='Test Contenido'
        )
        libro.categoria.add(categoria)

    def test_titulo_label(self):
        libro = Libro.objects.get(id=1)
        field_label = libro._meta.get_field('titulo').verbose_name
        self.assertEqual(field_label, 'titulo')

    def test_autor_max_length(self):
        libro = Libro.objects.get(id=1)
        max_length = libro._meta.get_field('autor').max_length
        self.assertEqual(max_length, 50)

    def test_isbn_max_length(self):
        libro = Libro.objects.get(id=1)
        max_length = libro._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 20)

    def test_object_name_is_titulo(self):
        libro = Libro.objects.get(id=1)
        expected_object_name = f'{libro.titulo}'
        self.assertEqual(expected_object_name, str(libro))

    def test_libro_tiene_categoria(self):
        libro = Libro.objects.get(id=1)
        self.assertTrue(libro.categoria.count() > 0)
