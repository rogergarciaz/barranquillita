import pytz
import datetime

# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.forms.models import model_to_dict
from django.db.models import F
from django.db.models import Q

# Models
from clientes.models import Compra, Cliente
from sueldos.models import Descripcion

# Forms
from clientes.forms import CompraForm


# Create your views here.
@login_required
def create_sale_model_form(request):
    clientes = Cliente.objects.all()
    CompraFormSet = formset_factory(CompraForm, extra=1)  # can_delete=True,
    if request.method == 'POST':
        venta = Compra.objects.last().venta + 1
        formset = CompraFormSet(request.POST)
        # if formset.is_valid():
        for form in formset:
            if form.is_valid():
                factura = form.save(commit=False)
                factura.usuario = request.user
                factura.perfil = request.user.perfil
                factura.modificado_por = request.user.username
                factura.venta = venta
                numero = form.cleaned_data.get('descripcion', None).pk
                descripcion = Descripcion.objects.get(pk=numero)
                cantidadA = descripcion.cantidad
                cantidad = form.cleaned_data.get('cantidad', None)
                resta = cantidadA - cantidad
                clienteid = int(request.POST['nombre'])
                precio = form.cleaned_data.get('precio_vendido', None)
                cliente = Cliente.objects.get(pk=clienteid)
                factura.nombre = cliente
                saldoA = cliente.saldo
                saldo = saldoA - precio*cantidad
                if resta >= 0 and cantidadA > 0:
                    descripcion.cantidad = resta
                    if factura.credito == True:
                        cliente.saldo = saldo
                        cliente.save()
                    descripcion.save()
                    factura.save()
                elif resta < 0 and cantidadA > 0:
                    descripcion.cantidad = 0
                    descripcion.save()
                    if factura.credito == True:
                        cliente.saldo = saldo
                        cliente.save()
                    factura.cantidad = cantidadA
                    factura.save()
                else:
                    descripcion.cantidad = resta
                    descripcion.save()
                    if factura.credito == True:
                        cliente.saldo = saldo
                        cliente.save()
                    factura.save()
        return redirect('facturav', factura=venta)
    return render(request, "clientes/ventas.html", {
        'formset': CompraFormSet,
        'clientes': clientes
    }
    )


@login_required
def create_bill(request, factura):
    ventas = Compra.objects.filter(venta=factura)
    cliente = ventas.last().nombre
    fecha = ventas.last().creado
    subtotal = []
    conteo = 1
    total = 0
    for venta in ventas:
        copia = model_to_dict(venta).copy()
        descrip = Descripcion.objects.get(pk=venta.descripcion.pk)
        copia['descripcion'] = descrip.nombre
        pesos = venta.precio_vendido * venta.cantidad
        if venta.credito == True:
            copia['credito'] = 'Si'
        else:
            copia['credito'] = 'No'
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
        'fecha': fecha.strftime('%Y-%m-%d %H:%M'),
    }
    )


@login_required
def see_consolidate(request):
    tabla = False
    fechaF = datetime.date.today()
    dia = datetime.timedelta(days=1)
    fechaI = fechaF
    fechaF = fechaF + dia
    ventas = Compra.objects.filter(creado__range=[fechaI, fechaF])
    tabla = True
    credito = 0
    efectivo = 0
    total = 0
    subtotal = []
    conteo = 1
    ventas = Compra.objects.filter(
        Q(creado__range=[fechaI, fechaF])
    )
    for venta in ventas:
        copia = model_to_dict(venta).copy()
        descrip = Descripcion.objects.get(pk=venta.descripcion.pk)
        copia['descripcion'] = descrip.nombre
        usua = User.objects.get(pk=venta.usuario.pk)
        copia['usuario'] = usua
        clien = Cliente.objects.get(pk=venta.nombre.pk)
        copia['nombre'] = clien
        valor = venta.cantidad * venta.precio_vendido
        if venta.credito == True:
            credito = credito + valor
            total = total + valor
            copia['credito'] = 'Si'
        else:
            efectivo = efectivo + valor
            total = total + valor
            copia['credito'] = 'No'
        copia['total'] = valor
        copia['numero'] = conteo
        subtotal.append(copia)
        conteo += 1
    return render(request, "clientes/acumulado.html", {
        'ventas': subtotal,
        'tabla': tabla,
        'credito': credito,
        'efectivo': efectivo,
        'total': total,
    }
    )

@login_required
def see_consolidateDates(request):
    tabla = False
    ventas = []
    if request.method == 'POST':
        initialDate = request.POST['fechaI'] #str '2020/10/08 17:02'
        inicialF = datetime.datetime.strptime(initialDate,"%Y/%m/%d %H:%M")
        finalDate = request.POST['fechaF']
        finalF = datetime.datetime.strptime(finalDate,"%Y/%m/%d %H:%M")
        tabla = True
        credito = 0
        efectivo = 0
        total = 0
        subtotal = []
        conteo = 1
        ventas = Compra.objects.filter(
            Q(creado__range=[inicialF, finalF])
        )
        for venta in ventas:
            copia = model_to_dict(venta).copy()
            descrip = Descripcion.objects.get(pk=venta.descripcion.pk)
            copia['descripcion'] = descrip.nombre
            usua = User.objects.get(pk=venta.usuario.pk)
            copia['usuario'] = usua
            clien = Cliente.objects.get(pk=venta.nombre.pk)
            copia['nombre'] = clien
            valor = venta.cantidad * venta.precio_vendido
            if venta.credito == True:
                credito = credito + valor
                total = total + valor
                copia['credito'] = 'Si'
            else:
                efectivo = efectivo + valor
                total = total + valor
                copia['credito'] = 'No'
            copia['total'] = valor
            copia['numero'] = conteo
            subtotal.append(copia)
            conteo += 1
        return render(request, "clientes/acumulado.html", {
            'ventas': subtotal,
            'tabla': tabla,
            'credito': credito,
            'efectivo': efectivo,
            'total': total,
        }
        )
    return render(request, "clientes/acumulado.html", {
        'ventas': ventas,
        'tabla': tabla,
    }
    )
