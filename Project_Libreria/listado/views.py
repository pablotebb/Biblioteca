from django.shortcuts import render
from libros.models import Libro

# Create your views here.
def home(request): 
  libros = Libro.objects.prefetch_related('criticas').all()
  listado_libros = list()

  for libro in libros:
    listado_libros.append(libro)
    
  
  return render(request, 'listado/home.html', {"listado": listado_libros})
