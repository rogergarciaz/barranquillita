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
from sueldos.models import Sueldo, Descripcion
from salarios.models import Produccion, Fijo
from prestamos.models import Prestamo
from usuarios.models import Perfil


# Create your views here
def sacar_sueldo(perfil, fechaI, fechaF, ver):
    valorP = 0
    valorF = 0
    valorD = 0
    # Agregando produccion
    producido = Produccion.objects.filter(
        usuario=perfil.usuario,
        creado__range=[fechaI, fechaF]
    )
    for produccion in producido:
        valorP = valorP + produccion.precio_pagado * produccion.cantidad
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
    if prestamos and ver:
        prestamos.update(cuotas_debidas=F('cuotas_debidas') - 1)
    # Valor total
    valor = valorP + valorF - valorD - perfil.seguro - perfil.recordar
    return valor, valorP, valorF, valorD


@login_required
def create_payment(request):
    nomina_antigua = Sueldo.objects.last()
    fechaI = nomina_antigua.creado
    if request.method == 'POST':
        ver = True  # reduce payments debts
        fechaF = datetime.datetime.now()  # not include day of click
        sueldo = nomina_antigua.sueldo + 1
        perfiles = Perfil.objects.filter(usuario__is_active=True)
        for perfil in perfiles:
            valor, valorP, valorF, valorD = sacar_sueldo(
                perfil, fechaI, fechaF, ver)
            nomina = Sueldo(
                usuario=perfil.usuario,
                perfil=perfil,
                nota=request.POST['nota'],
                sueldo=sueldo,
                valor=valor,
                agregado=request.user.username
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
        valor, valorP, valorF, valorD = sacar_sueldo(
            sueldo.perfil, fechaI, fechaF, ver)
        copia['empleado'] = str(sueldo.perfil.usuario.get_full_name())
        copia['valor'] = valor
        copia['valorP'] = valorP
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


def search_descriptions(request):
    descripciones = Descripcion.objects.filter(cantidad__lte=500)
    query = "Escribe la descripción"
    if request.method == 'POST':
        query = request.POST['description']
        if query.isnumeric():
            descripciones = Descripcion.objects.filter(
                Q(cantidad=query)
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
