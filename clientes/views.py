# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.forms.models import model_to_dict

# Models
from clientes.models import Compra, Cliente
from sueldos.models import Descripcion

# Forms
from clientes.forms import CompraForm

# Create your views here.
@login_required
def create_sale(request):
    # request.user.is_staff
    clientes = Cliente.objects.all()
    descripciones = Descripcion.objects.all()
    if request.method == 'POST':
        venta = Compra.objects.last().venta + 1
        form = CompraForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.usuario = request.user
            factura.perfil = request.user.perfil
            factura.venta = venta
            factura.save()
            return redirect('compra')
    else:
        form = CompraForm()
    return render(request, 'clientes/compra.html', {'clientes':clientes, 'descripciones':descripciones})

@login_required
def create_sale_model_form(request):
    CompraFormSet = formset_factory(CompraForm, extra=1)
    if request.method == 'POST':
        venta = Compra.objects.last().venta + 1
        formset = CompraFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                factura = form.save(commit=False)
                factura.usuario = request.user
                factura.perfil = request.user.perfil
                factura.venta = venta
                factura.save()
            return redirect('factura', factura=venta)
    return render(request, "clientes/compras.html", {
        'formset': CompraFormSet
        }
    )

@login_required
def create_bill(request, factura):
    compras = Compra.objects.filter(venta=factura)
    cliente = compras.last().nombre
    subtotal = []
    conteo = 1
    total = 0
    for compra in compras:
        copia = model_to_dict(compra).copy()
        descrip = Descripcion.objects.filter(nombre=compra.descripcion)
        copia['descripcion'] = descrip[0].nombre
        pesos = compra.precio_vendido * compra.cantidad
        copia['total'] = pesos
        copia['numero'] = conteo
        subtotal.append(copia)
        conteo += 1
        total = total + pesos
    return render(request, "clientes/factura.html", {
        'compras': subtotal,
        'cliente': cliente,
        'venta': factura,
        'total': total,
        }
    )