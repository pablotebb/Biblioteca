from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from libros.models import Libro, Categoria  # Asumimos que el modelo Libro existe en la app libros
from critica.models import Critica


class CriticaModelTest(TestCase):
    """Pruebas para el modelo Critica."""

    @classmethod
    def setUpTestData(cls):
        """Crea los datos iniciales para todas las pruebas de esta clase."""
        # Crear usuario y libro para establecer relaciones
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.categoria = Categoria.objects.create(nombre='Ficción')
        # CORRECCIÓN: El campo 'id_libros' debe ser una instancia de User.
        libro = Libro.objects.create(
            titulo='Libro de Prueba',
            autor='Autor de Prueba',
            id_libros=cls.user
        )
        libro.categoria.set([cls.categoria])
        cls.libro = libro
        # Crear la instancia de Critica
        cls.critica = Critica.objects.create(
            libro=cls.libro,
            usuario=cls.user,
            titulo='Gran Crítica',
            contenido='Este es un libro excelente.',
            puntuacion=5
        )

    def test_critica_creation(self):
        """Verifica que una instancia de Critica se crea correctamente."""
        self.assertIsInstance(self.critica, Critica)
        self.assertEqual(str(self.critica), 'Gran Crítica (Libro de Prueba)')

    def test_puntuacion_validation(self):
        """Verifica que la puntuación debe estar entre 1 y 5."""
        with self.assertRaises(ValidationError):
            critica_invalida = Critica(libro=self.libro, usuario=self.user, titulo='Título', contenido='Contenido', puntuacion=6)
            critica_invalida.full_clean()  # Lanza la validación del modelo