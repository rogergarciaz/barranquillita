import pytz
import datetime

# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.forms.models import model_to_dict

# Models
from proveedores.models import Adquisicion, Proveedor
from sueldos.models import DescripcionInterna

# Forms
from proveedores.forms import AdquisicionForm


# Create your views here.
@login_required
def create_adquisition_model_form(request):
    AdquisicionFormSet = formset_factory(AdquisicionForm, extra=10)
    proveedores = Proveedor.objects.all()
    if request.method == 'POST':
        compra = Adquisicion.objects.last().compra + 1
        formset = AdquisicionFormSet(request.POST)
        # if formset.is_valid():
        for form in formset:
            if form.is_valid():
                factura = form.save(commit=False)
                factura.usuario = request.user
                factura.perfil = request.user.perfil
                factura.compra = compra
                factura.modificado_por = request.user.username
                descripcionid = form.cleaned_data.get('descripcion', None).pk
                descripcion = DescripcionInterna.objects.get(pk=descripcionid)
                cantidadA = descripcion.cantidad
                cantidad = form.cleaned_data.get('cantidad', None)
                suma = cantidadA + cantidad
                proveedorid = int(request.POST['nombre'])
                precio = form.cleaned_data.get('precio_compra', None)
                proveedor = Proveedor.objects.get(pk=proveedorid)
                factura.nombre = proveedor
                saldoA = proveedor.saldo
                saldo = saldoA + precio*cantidad
                descripcion.cantidad = suma
                proveedor.saldo = saldo
                proveedor.save()
                descripcion.save()
                factura.save()
        return redirect('facturac', factura=compra)
    return render(request, "proveedores/compras.html", {
        'proveedores': proveedores,
        'formset': AdquisicionFormSet
    }
    )


@login_required
def create_bill(request, factura):
    compras = Adquisicion.objects.filter(compra=factura)
    proveedor = compras.last().nombre
    fecha = compras.last().creado
    subtotal = []
    conteo = 1
    total = 0
    for compra in compras:
        copia = model_to_dict(compra).copy()
        descrip = DescripcionInterna.objects.get(pk=compra.descripcion.pk)
        copia['descripcion'] = descrip.nombre
        pesos = compra.precio_compra * compra.cantidad
        if compra.credito == True and compra.credito_cancelado == True:
            copia['credito'] = 'Si'
            copia['credito_cancelado'] = 'Si'
        elif compra.credito == True and compra.credito_cancelado == False:
            copia['credito'] = 'Si'
            copia['credito_cancelado'] = 'No'
        else:
            copia['credito'] = 'No'
            copia['credito_cancelado'] = 'No aplica'
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
    compras = Adquisicion.objects.filter(
        cancelado=False, creado__range=[fechaI, fechaF])
    tabla = True
    credito = 0
    cancelado = 0
    efectivo = 0
    total = 0
    subtotal = []
    conteo = 1
    for compra in compras:
        copia = model_to_dict(compra).copy()
        descrip = DescripcionInterna.objects.get(pk=compra.descripcion.pk)
        copia['descripcion'] = descrip.nombre
        usua = User.objects.get(pk=compra.usuario.pk)
        copia['usuario'] = usua
        prove = Proveedor.objects.get(pk=compra.nombre.pk)
        copia['nombre'] = prove
        valor = compra.cantidad * compra.precio_compra
        if compra.credito == True and compra.credito_cancelado == True:
            cancelado = cancelado + valor
            total = total + valor
            copia['credito'] = 'Si'
            copia['credito_cancelado'] = 'Si'
        elif compra.credito == True and compra.credito_cancelado == False:
            credito = credito + valor
            total = total + valor
            copia['credito'] = 'Si'
            copia['credito_cancelado'] = 'No'
        else:
            efectivo = efectivo + valor
            total = total + valor
            copia['credito'] = 'No'
            copia['credito_cancelado'] = 'No aplica'
        copia['total'] = valor
        copia['numero'] = conteo
        subtotal.append(copia)
        conteo += 1
    return render(request, "proveedores/acumulado.html", {
        'compras': subtotal,
        'tabla': tabla,
        'credito': credito,
        'cancelado': cancelado,
        'efectivo': efectivo,
        'total': total,
    }
    )


@login_required
def see_consolidateDates(request):
    tabla = False
    compras = []
    if request.method == 'POST':
        initialDate = request.POST['fechaI']  # str '2020/10/08 17:02'
        inicialF = datetime.datetime.strptime(initialDate, "%Y/%m/%d %H:%M")
        finalDate = request.POST['fechaF']
        finalF = datetime.datetime.strptime(finalDate, "%Y/%m/%d %H:%M")
        tabla = True
        credito = 0
        cancelado = 0
        efectivo = 0
        total = 0
        subtotal = []
        conteo = 1
        compras = Adquisicion.objects.filter(
            cancelado=False, creado__range=[inicialF, finalF])
        for compra in compras:
            copia = model_to_dict(compra).copy()
            descrip = DescripcionInterna.objects.get(pk=compra.descripcion.pk)
            copia['descripcion'] = descrip.nombre
            usua = User.objects.get(pk=compra.usuario.pk)
            copia['usuario'] = usua
            prove = Proveedor.objects.get(pk=compra.nombre.pk)
            copia['nombre'] = prove
            valor = compra.cantidad * compra.precio_compra
            if compra.credito == True and compra.credito_cancelado == True:
                cancelado = cancelado + valor
                total = total + valor
                copia['credito'] = 'Si'
                copia['credito_cancelado'] = 'Si'
            elif compra.credito == True and compra.credito_cancelado == False:
                credito = credito + valor
                total = total + valor
                copia['credito'] = 'Si'
                copia['credito_cancelado'] = 'No'
            else:
                efectivo = efectivo + valor
                total = total + valor
                copia['credito'] = 'No'
                copia['credito_cancelado'] = 'No aplica'
            copia['total'] = valor
            copia['numero'] = conteo
            subtotal.append(copia)
            conteo += 1
        return render(request, "proveedores/acumulado.html", {
            'compras': subtotal,
            'tabla': tabla,
            'credito': credito,
            'cancelado': cancelado,
            'efectivo': efectivo,
            'total': total,
        }
        )
    return render(request, "proveedores/acumulado.html", {
        'compras': compras,
        'tabla': tabla,
    }
    )


@login_required
def cancel_bill(request):
    tabla = False
    mensaje = ' '
    if request.method == 'POST':
        numeroF = int(request.POST['compra'])
        compras = Adquisicion.objects.filter(compra=numeroF)
        for compra in compras:
            if compra.cancelado == False:
                compra.cancelado = True
                numero = compra.descripcion.pk
                descripcion = DescripcionInterna.objects.get(pk=numero)
                cantidadA = descripcion.cantidad
                cantidad = compra.cantidad
                resta = cantidadA - cantidad
                proveedorid = compra.nombre.pk
                precio = compra.precio_vendido
                proveedor = Proveedor.objects.get(pk=proveedorid)
                saldoA = proveedor.saldo
                saldo = saldoA - precio*cantidad
                descripcion.cantidad = resta
                if compra.credito == True:
                    proveedor.saldo = saldo
                    proveedor.save()
                descripcion.save()
                compra.save()
                mensaje = 'Se canceló la factura ' + str(numeroF)
                tabla = True
        return render(request, "proveedores/cancelado.html", {
            'mensaje': mensaje,
            'tabla': tabla,
        }
        )
    return render(request, "proveedores/cancelado.html", {
        'mensaje': mensaje,
        'tabla': tabla,
    }
    )


@login_required
def pay_bill(request):
    tabla = False
    mensaje = ' '
    if request.method == 'POST':
        numeroF = int(request.POST['compra'])
        compras = Adquisicion.objects.filter(compra=numeroF)
        for compra in compras:
            if compra.credito_cancelado == False and compra.credito == True and compra.cancelado == False:
                compra.credito_cancelado = True
                cantidad = compra.cantidad
                proveedorid = compra.nombre.pk
                precio = compra.precio_compra
                proveedor = Proveedor.objects.get(pk=proveedorid)
                saldoA = proveedor.saldo
                saldo = saldoA - precio*cantidad
                proveedor.saldo = saldo
                proveedor.save()
                compra.save()
                mensaje = 'Se pagó la factura ' + str(numeroF)
                tabla = True
        return render(request, "proveedores/cancelado.html", {
            'mensaje': mensaje,
            'tabla': tabla,
        }
        )
    return render(request, "proveedores/cancelado.html", {
        'mensaje': mensaje,
        'tabla': tabla,
    }
    )


@login_required
def pay_product(request):
    tabla = False
    mensaje = ' '
    if request.method == 'POST':
        numeroF = int(request.POST['compra'])
        compra = Adquisicion.objects.get(pk=numeroF)
        if compra.credito_cancelado == False and compra.credito == True and compra.cancelado == False:
            compra.credito_cancelado = True
            cantidad = compra.cantidad
            proveedorid = compra.nombre.pk
            precio = compra.precio_compra
            proveedor = Proveedor.objects.get(pk=proveedorid)
            saldoA = proveedor.saldo
            saldo = saldoA - precio*cantidad
            proveedor.saldo = saldo
            proveedor.save()
            compra.save()
            mensaje = 'Se pagó el producto' + str(numeroF)
            tabla = True
        return render(request, "proveedores/cancelado.html", {
            'mensaje': mensaje,
            'tabla': tabla,
        }
        )
    return render(request, "proveedores/cancelado.html", {
        'mensaje': mensaje,
        'tabla': tabla,
    }
    )
