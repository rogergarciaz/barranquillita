# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Models
from ventas.models import Venta, Cliente
from sueldos.models import Descripcion

# Forms
from ventas.forms import VentaForm


# Create your views here.
@login_required
def create_sale(request):
    # request.user.is_staff
    clientes = Cliente.objects.all()
    descripciones = Descripcion.objects.all()
    if request.method == 'POST':
        venta = Venta.objects.last().venta + 1
        form = VentaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.usuario = request.user
            factura.perfil = request.user.perfil
            factura.venta = venta
            factura.save()
            return redirect('venta')
    else:
        form = VentaForm()
    return render(request, 'ventas/venta.html', {'clientes':clientes, 'descripciones':descripciones})