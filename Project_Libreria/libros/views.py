from django.shortcuts import render, get_object_or_404, redirect
from .models import Libro
from .forms import Formulario_libros

def libro_view(request):
  if request.method == 'POST':
    form = Formulario_libros(request.POST)
    if form.is_valid():
      print("Grabando un libro")
      libro = form.save(commit=False)
      libro.id_libros = request.user  # Asignamos el usuario logueado
      libro.save()
      form.save_m2m()  # Necesario para ManyToManyFields como 'categoria'
      return redirect('libro:libros')
    else:
      print("NO GRABA")
      print("Errores:", form.errors)
      print("Usuario actual:", request.user)
      print("¿Está autenticado?", request.user.is_authenticated)
      return redirect('libro:libros')
  else:
    form = Formulario_libros()

    libros = Libro.objects.all()  

    return render(request, 'libros/libro.html', {
        'form': form,
        'libros': libros,
    })

def editar_libro(request, pk):
  libro = get_object_or_404(Libro, pk=pk)
  if request.method == 'POST':
    form = Formulario_libros(request.POST, instance=libro)
    if form.is_valid():
      libro = form.save(commit=False)
      libro.id_libros = request.user
      libro.save()
      form.save_m2m()
      return redirect('libro:libros')
  else:
    form = Formulario_libros(instance=libro)
  return render(request, 'libros/formulario.html', {'form': form})

def borrar_libro(request, pk):
  libro = get_object_or_404(Libro, pk=pk)
  if request.method == 'POST':
    libro.delete()
    return redirect('libro:libros')
  return render(request, 'libros/confirmar_borrar.html', {'libro': libro})