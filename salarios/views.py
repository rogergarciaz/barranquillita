# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Models
from sueldos.models import Descripcion, DescripcionInterna
from usuarios.models import Perfil
# Forms
from salarios.forms import ProductionForm, ProductionInternaForm, FijoForm


# Create your views here.
@login_required
def create_product(request):
    usuarios = Perfil.objects.all()
    #usuarios = User.objects.all()
    include_list = ['Sellado', 'Extrusion']
    descripciones = Descripcion.objects.filter(area__in=include_list)
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            produccion = form.save(commit=False)
            produccion.agregado = request.user.username
            produccion.modificado_por = request.user.username
            produccion.save()
            numero = form.cleaned_data.get('descripcion', None).pk
            descripcion = Descripcion.objects.get(pk=numero)
            cantidadA = descripcion.cantidad
            descripcion.cantidad = cantidadA + \
                form.cleaned_data.get('cantidad', None)
            descripcion.save()
            return redirect('producto')
    else:
        form = ProductionForm()
    return render(request, 'salarios/producto.html', {'usuarios': usuarios, 'descripciones': descripciones})


@login_required
def create_production(request):
    usuarios = Perfil.objects.all()
    #usuarios = User.objects.all()
    exclude_list = ['Sellado', 'Extrusion']
    descripciones = DescripcionInterna.objects.exclude(area__in=exclude_list)
    if request.method == 'POST':
        form = ProductionInternaForm(request.POST)
        if form.is_valid():
            produccion = form.save(commit=False)
            produccion.agregado = request.user.username
            produccion.modificado_por = request.user.username
            produccion.save()
            numero = form.cleaned_data.get('descripcion', None).pk
            descripcion = DescripcionInterna.objects.get(pk=numero)
            cantidadA = descripcion.cantidad
            descripcion.cantidad = cantidadA + \
                form.cleaned_data.get('cantidad', None)
            descripcion.save()
            return redirect('produccion')
    else:
        form = ProductionInternaForm()
    return render(request, 'salarios/produccion.html', {'usuarios': usuarios, 'descripciones': descripciones})


@login_required
def take_production(request):
    usuarios = Perfil.objects.all()
    #usuarios = User.objects.all()
    exclude_list = ['Sellado', 'Extrusion']
    descripciones = DescripcionInterna.objects.exclude(area__in=exclude_list)
    if request.method == 'POST':
        form = ProductionInternaForm(request.POST)
        if form.is_valid():
            produccion = form.save(commit=False)
            produccion.agregado = request.user.username
            produccion.modificado_por = request.user.username
            produccion.save()
            numero = form.cleaned_data.get('descripcion', None).pk
            descripcion = DescripcionInterna.objects.get(pk=numero)
            cantidadA = descripcion.cantidad
            descripcion.cantidad = cantidadA - \
                form.cleaned_data.get('cantidad', None)
            descripcion.save()
            return redirect('sacado')
    else:
        form = ProductionInternaForm()
    return render(request, 'salarios/sacado.html', {'usuarios': usuarios, 'descripciones': descripciones})


@login_required
def create_assistance(request):
    usuarios = Perfil.objects.all()
    #usuarios = User.objects.all()
    if request.method == 'POST':
        form = FijoForm(request.POST)
        if form.is_valid():
            asistencia = form.save(commit=False)
            asistencia.agregado = request.user.username
            asistencia.modificado_por = request.user.username
            asistencia.save()
            return redirect('asistencia')
    else:
        form = FijoForm()
    return render(request, 'salarios/asistencia.html', {'usuarios': usuarios})
