from django import forms
from .models import Libro

class Formulario_libros(forms.ModelForm):
  class Meta:
    model = Libro
    exclude = ['id_libros']  # Excluimos el campo del formulario
    widgets = {
      'categoria': forms.SelectMultiple(attrs={'class': 'form-control'}),
      'isbn': forms.TextInput(attrs={'class': 'form-control'}),
      'titulo': forms.TextInput(attrs={'class': 'form-control'}),
      'autor': forms.TextInput(attrs={'class': 'form-control'}),
      'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
      'imagen': forms.FileInput(attrs={'class': 'form-control'}),
      'leido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
   

    