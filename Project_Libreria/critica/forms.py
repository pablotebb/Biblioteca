from django import forms
from .models import Critica


class Formulario_critica(forms.ModelForm):
  class Meta:
    model = Critica
    # Excluimos campos que se asignarán automáticamente (usuario, fechas)
    fields = ['libro', 'titulo', 'contenido', 'puntuacion']
    widgets = {
      'libro': forms.Select(attrs={'class': 'form-control'}),
      'titulo': forms.TextInput(attrs={'class': 'form-control'}),
      'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
      'puntuacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
    }