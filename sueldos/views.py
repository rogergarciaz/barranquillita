from django.utils import timezone
import pytz


# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from prestamos.forms import PrestamoForm
from django.db.models import F

# Models
from sueldos.models import Sueldo
from salarios.models import Produccion, Fijo
from prestamos.models import Prestamo
from usuarios.models import Perfil


# Create your views here.
def sacar_sueldo(perfil, fechaI, fechaF):
    valorP = 0
    valorF = 0
    valorD = 0
    #import pdb; pdb.set_trace()
    ## Agregando produccion
    producido = Produccion.objects.filter(
        usuario= perfil.usuario,
        creado__range= [fechaI, fechaF]
        )
    for produccion in producido:
        valorP = valorP + produccion.precio_pagado * produccion.cantidad
    ## Agregando por dia
    fijos = Fijo.objects.filter(
        usuario= perfil.usuario,
        creado__range= [fechaI, fechaF]
        )
    for fijo in fijos:
        valorF = valorF + fijo.precio_pagado
    ## Agregando prestamos
    prestamos = Prestamo.objects.filter(
        usuario= perfil.usuario,
        cuotas_debidas__gt= 0,
        )
    for prestamo in prestamos:
        valorD = valorD + prestamo.valor/prestamo.cuotas
    if prestamos:
        prestamos.update(cuotas_debidas= F('cuotas_debidas') - 1)
    ## Valor Total
    valor = valorP + valorF - valorD - perfil.seguro - perfil.recordar
    return valor

@login_required
def create_payment(request):
    nomina_antigua = Sueldo.objects.last()
    fechaI = nomina_antigua.creado
    if request.method == 'POST':
        fechaF = timezone.now()
        sueldo = nomina_antigua.sueldo + 1
        perfiles = Perfil.objects.filter(usuario__is_active=True)
        for perfil in perfiles:
            valor = sacar_sueldo(perfil, fechaI, fechaF)
            nomina = Sueldo(
                usuario=perfil.usuario,
                perfil=perfil,
                nota=request.POST['nota'],
                sueldo=sueldo,
                valor=valor,
            )
            nomina.save()
        return redirect('nomina')
    return render(request, 'sueldos/nomina.html')