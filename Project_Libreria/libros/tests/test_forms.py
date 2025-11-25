from django.test import TestCase
from django import forms
from ..forms import Formulario_libros
from ..models import Categoria, User
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

class FormularioLibrosTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.categoria = Categoria.objects.create(nombre='Aventura')

    def test_form_valid(self):
        # Create a temporary image file for testing
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            img = Image.new('RGB', (10, 10))
            img.save(tmp, 'jpeg')
            tmp.seek(0)
            image = SimpleUploadedFile(tmp.name, tmp.read(), content_type='image/jpeg')

        form_data = {
            'isbn': '123-4567890123',
            'autor': 'Autor de Prueba',
            'titulo': 'Libro de Prueba',
            'contenido': 'Contenido de prueba.',
            'categoria': [self.categoria.pk],
        }
        form = Formulario_libros(data=form_data, files={'imagen': image})
        
        if not form.is_valid():
             self.fail(f"Form was not valid: {form.errors}")
        self.assertTrue(form.is_valid())


    def test_form_invalid(self):
        form_data = {
            'isbn': '',  # ISBN is required
            'autor': 'Autor de Prueba',
            'titulo': 'Libro de Prueba',
            'contenido': 'Contenido de prueba.',
        }
        form = Formulario_libros(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_widgets(self):
        form = Formulario_libros()
        self.assertIsInstance(form.fields['categoria'].widget, forms.SelectMultiple)
        self.assertIsInstance(form.fields['isbn'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['titulo'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['autor'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['contenido'].widget, forms.Textarea)
        self.assertIsInstance(form.fields['imagen'].widget, forms.FileInput)
