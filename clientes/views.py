# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.forms.models import model_to_dict
#from django.db.models import F

# Models
from clientes.models import Compra, Cliente
from sueldos.models import Descripcion

# Forms
from clientes.forms import CompraForm

# Create your views here.
@login_required
def create_sale(request):
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
            numero = form.cleaned_data.get('descripcion', None).pk
            descripcion = Descripcion.objects.get(pk=numero)
            cantidadA = descripcion.cantidad
            cantidad = form.cleaned_data.get('cantidad', None)
            resta = cantidadA - cantidad
            clienteid = form.cleaned_data.get('nombre', None).pk
            precio = form.cleaned_data.get('precio_vendido', None)
            cliente = Cliente.objects.get(pk=clienteid)
            saldoA = cliente.saldo
            saldo = saldoA - precio*cantidad
            if resta >= 0 and cantidadA > 0:
                descripcion.cantidad = resta
                cliente.saldo = saldo
                cliente.save()
                descripcion.save()
                factura.save()
            elif resta < 0 and cantidadA > 0:
                descripcion.cantidad = 0
                descripcion.save()
                cliente.saldo = saldo
                cliente.save()
                factura.cantidad = cantidadA
                factura.save()
            else:
                descripcion.cantidad = resta
                descripcion.save()
                cliente.saldo = saldo
                cliente.save()
                factura.save()

            
            return redirect('venta')
    else:
        form = CompraForm()
    return render(request, 'clientes/venta.html', {'clientes':clientes, 'descripciones':descripciones})

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
                numero = form.cleaned_data.get('descripcion', None).pk
                descripcion = Descripcion.objects.get(pk=numero)
                cantidadA = descripcion.cantidad
                cantidad = form.cleaned_data.get('cantidad', None)
                resta = cantidadA - cantidad
                clienteid = form.cleaned_data.get('nombre', None).pk
                precio = form.cleaned_data.get('precio_vendido', None)
                cliente = Cliente.objects.get(pk=clienteid)
                saldoA = cliente.saldo
                saldo = saldoA - precio*cantidad
                if resta >= 0 and cantidadA > 0:
                    descripcion.cantidad = resta
                    cliente.saldo = saldo
                    cliente.save()
                    descripcion.save()
                    factura.save()
                elif resta < 0 and cantidadA > 0:
                    descripcion.cantidad = 0
                    descripcion.save()
                    cliente.saldo = saldo
                    cliente.save()
                    factura.cantidad = cantidadA
                    factura.save()
                else:
                    descripcion.cantidad = resta
                    descripcion.save()
                    cliente.saldo = saldo
                    cliente.save()
                    factura.save()
            return redirect('facturav', factura=venta)
    return render(request, "clientes/ventas.html", {
        'formset': CompraFormSet
        }
    )

@login_required
def create_bill(request, factura):
    ventas = Compra.objects.filter(venta=factura)
    cliente = ventas.last().nombre
    subtotal = []
    conteo = 1
    total = 0
    for venta in ventas:
        copia = model_to_dict(venta).copy()
        descrip = Descripcion.objects.get(pk=venta.descripcion.pk)
        copia['descripcion'] = descrip.nombre
        pesos = venta.precio_vendido * venta.cantidad
        copia['total'] = pesos
        copia['numero'] = conteo
        subtotal.append(copia)
        conteo += 1
        total = total + pesos
    return render(request, "clientes/factura.html", {
        'ventas': subtotal,
        'cliente': cliente,
        'venta': factura,
        'total': total,
        }
    )