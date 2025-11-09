from django.test import TestCase
from critica.forms import Formulario_critica
from django.contrib.auth.models import User
from libros.models import Libro, Categoria


class CriticaFormTest(TestCase):
    """Pruebas para el formulario Formulario_critica."""

    @classmethod
    def setUpTestData(cls):
        """Crea un libro para usarlo en las pruebas del formulario."""
        cls.user = User.objects.create_user(username='formuser', password='password')
        cls.categoria = Categoria.objects.create(nombre='Formulario Test')
        # CORRECCIÓN: El campo 'id_libros' debe ser una instancia de User.
        cls.libro = Libro.objects.create(
            titulo='Libro para Formulario',
            autor='Autor',
            id_libros=cls.user)
        cls.libro.categoria.set([cls.categoria])

    def test_form_is_valid(self):
        """Prueba que el formulario es válido con datos correctos."""
        form_data = {
            'libro': self.libro.id,
            'titulo': 'Un título válido',
            'contenido': 'Un contenido de crítica detallado y completo.',
            'puntuacion': 4
        }
        form = Formulario_critica(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_when_fields_are_missing(self):
        """Prueba que el formulario es inválido si faltan campos requeridos."""
        form_data = {'titulo': 'Solo título'}
        form = Formulario_critica(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('libro', form.errors)
        self.assertIn('contenido', form.errors)
        self.assertIn('puntuacion', form.errors)

    def test_form_has_expected_fields(self):
        """Verifica que el formulario contiene los campos esperados."""
        form = Formulario_critica()
        expected_fields = ['libro', 'titulo', 'contenido', 'puntuacion']
        self.assertEqual(list(form.fields.keys()), expected_fields)