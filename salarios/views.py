# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Models
from sueldos.models import Descripcion

# Forms
from salarios.forms import ProductionForm, FijoForm


# Create your views here.
@login_required
def create_production(request):
    usuarios = User.objects.all()
    descripciones = Descripcion.objects.all()
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            produccion = form.save(commit=False)
            produccion.agregado = request.user.username
            produccion.save()
            numero = form.cleaned_data.get('descripcion', None).pk
            descripcion = Descripcion.objects.get(pk=numero)
            cantidadA = descripcion.cantidad
            descripcion.cantidad = cantidadA + \
                form.cleaned_data.get('cantidad', None)
            descripcion.save()
            return redirect('produccion')
    else:
        form = ProductionForm()
    return render(request, 'salarios/produccion.html', {'usuarios': usuarios, 'descripciones': descripciones})


@login_required
def create_assistance(request):
    usuarios = User.objects.all()
    if request.method == 'POST':
        form = FijoForm(request.POST)
        if form.is_valid():
            asistencia = form.save(commit=False)
            asistencia.agregado = request.user.username
            asistencia.save()
            return redirect('asistencia')
    else:
        form = FijoForm()
    return render(request, 'salarios/asistencia.html', {'usuarios': usuarios})
