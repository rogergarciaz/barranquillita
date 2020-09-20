# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.forms.models import model_to_dict
#from django.db.models import F

# Models
from proveedores.models import Adquisicion, Proveedor
from sueldos.models import Descripcion

# Forms
from proveedores.forms import AdquisicionForm

# Create your views here.
@login_required
def create_adquisition(request):
    proveedores = Proveedor.objects.all()
    descripciones = Descripcion.objects.all()
    if request.method == 'POST':
        compra = Adquisicion.objects.last().compra + 1
        form = AdquisicionForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.usuario = request.user
            factura.perfil = request.user.perfil
            factura.compra = compra
            descripcionid = form.cleaned_data.get('descripcion', None).pk
            descripcion = Descripcion.objects.get(pk=descripcionid)
            cantidadA = descripcion.cantidad
            cantidad = form.cleaned_data.get('cantidad', None)
            suma = cantidadA + cantidad
            proveedorid = form.cleaned_data.get('nombre', None).pk
            precio = form.cleaned_data.get('precio_compra', None)
            proveedor = Proveedor.objects.get(pk=proveedorid)
            saldoA = proveedor.saldo
            saldo = saldoA + precio*cantidad
            descripcion.cantidad = suma
            proveedor.saldo = saldo
            proveedor.save()
            descripcion.save()
            factura.save()
            return redirect('compra')
    else:
        form = AdquisicionForm()
    return render(request, 'proveedores/compra.html', {'proveedores':proveedores, 'descripciones':descripciones})

@login_required
def create_adquisition_model_form(request):
    AdquisicionFormSet = formset_factory(AdquisicionForm, extra=1)
    if request.method == 'POST':
        compra = Adquisicion.objects.last().compra + 1
        formset = AdquisicionFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                factura = form.save(commit=False)
                factura.usuario = request.user
                factura.perfil = request.user.perfil
                factura.compra = compra
                descripcionid = form.cleaned_data.get('descripcion', None).pk
                descripcion = Descripcion.objects.get(pk=descripcionid)
                cantidadA = descripcion.cantidad
                cantidad = form.cleaned_data.get('cantidad', None)
                suma = cantidadA + cantidad
                proveedorid = form.cleaned_data.get('nombre', None).pk
                precio = form.cleaned_data.get('precio_compra', None)
                proveedor = Proveedor.objects.get(pk=proveedorid)
                saldoA = proveedor.saldo
                saldo = saldoA + precio*cantidad
                descripcion.cantidad = suma
                proveedor.saldo = saldo
                proveedor.save()
                descripcion.save()
                factura.save()
            return redirect('facturac', factura=compra)
    return render(request, "proveedores/compras.html", {
        'formset': AdquisicionFormSet
        }
    )

@login_required
def create_bill(request, factura):
    compras = Adquisicion.objects.filter(compra=factura)
    proveedor = compras.last().nombre
    subtotal = []
    conteo = 1
    total = 0
    for compra in compras:
        copia = model_to_dict(compra).copy()
        descrip = Descripcion.objects.get(pk=compra.descripcion.pk)
        copia['descripcion'] = descrip.nombre
        pesos = compra.precio_compra * compra.cantidad
        copia['total'] = pesos
        copia['numero'] = conteo
        subtotal.append(copia)
        conteo += 1
        total = total + pesos
    return render(request, "proveedores/factura.html", {
        'compras': subtotal,
        'proveedor': proveedor,
        'compra': factura,
        'total': total,
        }
    )