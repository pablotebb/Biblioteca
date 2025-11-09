from django.shortcuts import render, get_object_or_404, redirect
from .models import Critica 
from libros.models import Libro
from .forms import Formulario_critica
from django.contrib.auth.decorators import login_required



def critica_view(request):
    if request.method == 'POST':
        # Si el método es POST, siempre se procesa el formulario enviado.
        form = Formulario_critica(request.POST)
        if form.is_valid():
            critica = form.save(commit=False)
            critica.usuario = request.user
            critica.save()
            return redirect('critica:critica')
        # Si el formulario NO es válido, la ejecución no entra en el if,
        # y la vista renderizará la plantilla con este mismo objeto 'form' que contiene los errores.
    else:
        # Si el método es GET, se crea un formulario vacío.
        form = Formulario_critica()

    criticas = Critica.objects.all()
    return render(request, 'critica/critica.html', {'form': form, 'criticas': criticas})


def editar_critica(request, pk):    
    critica = get_object_or_404(Critica, pk=pk)    
    if request.method == 'POST':        
        form = Formulario_critica(request.POST, instance=critica)        
        if form.is_valid():            
          form.save()            
          return redirect('critica:critica')    
    else:        
        form = Formulario_critica(instance=critica)    
    return render(request, 'critica/formulario.html', {'form': form})


def borrar_critica(request, pk):    
    critica = get_object_or_404(Critica, pk=pk)    
    if request.method == 'POST':        
      critica.delete()        
      return redirect('../../../critica')    
    return render(request, 'critica/confirmar_borrar.html', {'critica': critica})
