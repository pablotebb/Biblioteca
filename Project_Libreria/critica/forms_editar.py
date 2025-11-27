from django import forms
from .models import Critica


class Formulario_critica_editar(forms.ModelForm):
  class Meta:
    model = Critica
    fields = ['libro', 'contenido']
    widgets = {
      'libro': forms.TextInput(attrs={'class': 'form-control'}),
      'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    }    