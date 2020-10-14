import pytz
import datetime

# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from prestamos.forms import PrestamoForm
from django.db.models import F
from django.http import FileResponse
from django.http import HttpResponse
from django.conf import settings
from django.forms.models import model_to_dict
from django.views.generic import TemplateView, ListView
from django.db.models import Q

# Models
from sueldos.models import Sueldo, Descripcion, DescripcionInterna
from salarios.models import Produccion, ProduccionInterna, Fijo
from prestamos.models import Prestamo
from usuarios.models import Perfil


# Create your views here
def sacar_sueldo(perfil, fechaI, fechaF, ver):
    valorP = 0
    valorF = 0
    valorD = 0
    valorI = 0
    existeD = 0
    # Agregando produccion
    producido = Produccion.objects.filter(
        usuario=perfil.usuario,
        creado__range=[fechaI, fechaF]
    )
    for produccion in producido:
        valorP = valorP + produccion.precio_pagado * produccion.cantidad
    # Agregando produccion interna
    producidoInterno = ProduccionInterna.objects.filter(
        usuario=perfil.usuario,
        ingresado=True,
        creado__range=[fechaI, fechaF]
    )
    for produccionI in producidoInterno:
        valorI = valorI + produccionI.precio_pagado * produccionI.cantidad
    # Agregando por dia
    fijos = Fijo.objects.filter(
        usuario=perfil.usuario,
        creado__range=[fechaI, fechaF]
    )
    for fijo in fijos:
        valorF = valorF + fijo.precio_pagado
    # Agregando prestamos
    prestamos = Prestamo.objects.filter(
        usuario=perfil.usuario,
        cuotas_debidas__gt=0,
    )
    for prestamo in prestamos:
        valorD = valorD + prestamo.valor/prestamo.cuotas
        existeD = existeD + 1
    if existeD > 0 and ver:
        prestamos.update(cuotas_debidas=F('cuotas_debidas') - 1)
    # Valor total
    valor = valorP + valorF + valorI - valorD - perfil.seguro - perfil.recordar
    return valor, valorP, valorF, valorD, valorI


@login_required
def create_payment(request):
    if request.method == 'POST':
        nomina_antigua = Sueldo.objects.last()
        fechaI = nomina_antigua.creado
        ver = True  # reduce payments debts
        fechaF = datetime.datetime.now()  # not include day of click
        sueldo = nomina_antigua.sueldo + 1
        perfiles = Perfil.objects.filter(usuario__is_active=True)
        for perfil in perfiles:
            valor, valorP, valorF, valorD, valorI = sacar_sueldo(
                perfil, fechaI, fechaF, ver)
            nomina = Sueldo(
                usuario=perfil.usuario,
                perfil=perfil,
                nota=request.POST['nota'],
                sueldo=sueldo,
                valor=valor,
                agregado=request.user.username,
                modificado_por=request.user.username
            )
            nomina.save()
        return redirect('nominas', nomina=sueldo)
    return render(request, 'sueldos/nomina.html')


@login_required
def see_payment(request, nomina):
    ver = False  # not reduce payment debts
    sueldos = Sueldo.objects.filter(sueldo=nomina)
    fechaI = Sueldo.objects.filter(
        sueldo=nomina-1).last().creado + datetime.timedelta(seconds=3)
    fechaF = sueldos.last().creado + datetime.timedelta(seconds=3)
    subtotal = []
    conteo = 1
    total = 0
    for sueldo in sueldos:
        copia = model_to_dict(sueldo).copy()
        valor, valorP, valorF, valorD, valorI = sacar_sueldo(
            sueldo.perfil, fechaI, fechaF, ver)
        valorD = valor - sueldo.valor
        copia['empleado'] = str(sueldo.perfil.usuario.get_full_name())
        copia['valor'] = valor - valorD
        copia['valorP'] = valorP + valorI
        copia['valorF'] = valorF
        copia['valorD'] = valorD
        copia['numero'] = conteo
        subtotal.append(copia)
        conteo += 1
        total = total + valor
    return render(request, "sueldos/sueldo.html", {
        'sueldos': subtotal,
        'nomina': nomina,
        'total': total,
        'fechaIn': fechaI.strftime('%Y-%m-%d %H:%M'),
        'fechaFi': fechaF.strftime('%Y-%m-%d %H:%M'),
    }
    )


@login_required
def see_paymentDates(request):
    if request.method == 'POST':
        nomina = 'Especial'
        initialDate = request.POST['fechaI']  # str '2020/10/08 17:02'
        fechaI = datetime.datetime.strptime(initialDate, "%Y/%m/%d %H:%M")
        finalDate = request.POST['fechaF']
        fechaF = datetime.datetime.strptime(finalDate, "%Y/%m/%d %H:%M")
        ver = False  # not reduce payment debts
        sueldos = Sueldo.objects.filter(creado__range=[fechaI, fechaF])
        subtotal = []
        conteo = 1
        total = 0
        for sueldo in sueldos:
            copia = model_to_dict(sueldo).copy()
            valor, valorP, valorF, valorD, valorI = sacar_sueldo(
                sueldo.perfil, fechaI, fechaF, ver)
            copia['empleado'] = str(sueldo.perfil.usuario.get_full_name())
            copia['valor'] = valor
            copia['valorP'] = valorP + valorI
            copia['valorF'] = valorF
            copia['valorD'] = valorD
            copia['numero'] = conteo
            subtotal.append(copia)
            conteo += 1
            total = total + valor
        return render(request, "sueldos/sueldo.html", {
            'sueldos': subtotal,
            'nomina': nomina,
            'total': total,
            'fechaIn': fechaI.strftime('%Y-%m-%d %H:%M'),
            'fechaFi': fechaF.strftime('%Y-%m-%d %H:%M'),
        }
        )
    return render(request, 'sueldos/nomina.html')


def search_descriptions(request):
    descripciones = Descripcion.objects.filter(cantidad__lte=500)
    query = "Escribe la descripción"
    if request.method == 'POST':
        query = request.POST['description']
        if query.isnumeric():
            descripciones = Descripcion.objects.filter(
                Q(cantidad__lte=query)
            )
        else:
            descripciones = Descripcion.objects.filter(
                Q(nombre__icontains=query)
            )
        return render(request, "sueldos/buscar.html", {
            'descripciones': descripciones,
            'query': query,
        }
        )
    return render(request, "sueldos/buscar.html", {
        'descripciones': descripciones,
        'query': query,
    }
    )


def search_internal_descriptions(request):
    descripciones = DescripcionInterna.objects.filter(cantidad__lte=500)
    query = "Escribe la descripción"
    if request.method == 'POST':
        query = request.POST['description']
        if query.isnumeric():
            descripciones = DescripcionInterna.objects.filter(
                Q(cantidad__lte=query)
            )
        else:
            descripciones = DescripcionInterna.objects.filter(
                Q(nombre__icontains=query)
            )
        return render(request, "sueldos/buscarInterna.html", {
            'descripciones': descripciones,
            'query': query,
        }
        )
    return render(request, "sueldos/buscarInterna.html", {
        'descripciones': descripciones,
        'query': query,
    }
    )
