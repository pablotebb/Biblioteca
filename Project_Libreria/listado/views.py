from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from libros.models import Libro

# Create your views here.

@login_required(login_url="/autenticacion/logear")
def home(request):
  libros = Libro.objects.all()
  return render(request, 'listado/home.html', {"listado": libros})
