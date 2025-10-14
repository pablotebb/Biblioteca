from django.shortcuts import render
from .forms import Formulario_libros

# Create your views here.
def home(request):
    formulario_libros = Formulario_libros()
    return render(request, 'libros/home.html')