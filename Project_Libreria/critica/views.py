from django.shortcuts import render
from .forms import Formulario_critica

# Create your views here.
def home(request):
    Formulario_critica = Formulario_critica()
    return render(request, 'critica/home.html')
