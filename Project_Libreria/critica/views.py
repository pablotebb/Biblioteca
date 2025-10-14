from django.shortcuts import render
from .forms import Formulario_critica
from .critica import Critica_formulario
from libros.models import Libro

# Create your views here.
def home(request):
  formulario_critica = Formulario_critica()
  libros = Libro.objects.all()
  titulos = []
  for value in libros:
    # titulos.append(Critica_formulario(
    # producto_id = value.id_libros,
    # critica = value["contenido"]))
    titulos = value.contenido
  return render(request, 'critica/home.html', {"formulario": formulario_critica, "titulos": titulos})



