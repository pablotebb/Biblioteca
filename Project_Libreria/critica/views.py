from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Critica 
from libros.models import Libro
from .forms import Formulario_critica
from .forms_editar import Formulario_critica_editar

@login_required(login_url="/autenticacion/logear")
def critica_view(request):
    if request.method == 'POST':
        form = Formulario_critica(request.POST)
        if form.is_valid():
            form.save()
            return redirect('critica:critica')
            #return redirect('critica/')  # Redirigir a la misma página
    else:
        form = Formulario_critica()
        form.fields['libro'].queryset = Libro.objects.filter(leido=True)

    criticas = Critica.objects.filter(libro__leido=True)
    

    return render(request, 'critica/critica.html', {
        'form': form,
        'criticas': criticas,
    })

@login_required(login_url="/autenticacion/logear")
def editar_critica(request, pk):
    critica = get_object_or_404(Critica, pk=pk)
    if request.method == 'POST':
        form = Formulario_critica_editar(request.POST, instance=critica)
        if form.is_valid():
            form.save()
            return redirect('critica:critica')
    else:
        form = Formulario_critica_editar(instance=critica)
    return render(request, 'critica/formulario.html', {'form': form})

@login_required(login_url="/autenticacion/logear")
def borrar_critica(request, pk):
    critica = get_object_or_404(Critica, pk=pk)
    if request.method == 'POST':
        critica.delete()
        return redirect('../../../critica')
    return render(request, 'critica/confirmar_borrar.html', {'critica': critica})