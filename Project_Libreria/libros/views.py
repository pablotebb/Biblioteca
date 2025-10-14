from django.shortcuts import render
from .forms import Formulario_libros

# Create your views here.
def home(request):
  
  formulario_libro = Formulario_libros()
  
  if request.method=="POST":
    formulario_libro = Formulario_libros(data=request.POST)
    if formulario_libro.is_valid():
      isbn = request.POST.get("isbn")
      titulo = request.POST.get("titulo")
      autor = request.POST.get("autor")
      categoria = request.POST.get("categoria")
      contenido = request.POST.get("contenido")
      imagen = request.POST.get("imagen")
      
  
  return render(request, "libros/home.html", {"mi_formulario": formulario_libro})

