# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory

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

def create_sale_model_form(request):
    CompraFormSet = formset_factory(CompraForm, extra=1)
    if request.method == 'POST':
        venta = Compra.objects.last().venta + 1
        formset = CompraFormSet(request.POST)
        import pdb; pdb.set_trace()
        if formset.is_valid():
            for form in formset:
                factura = form.save(commit=False)
                factura.usuario = request.user
                factura.perfil = request.user.perfil
                factura.venta = venta
                if request.POST['eliminar'] != True:
                    factura.save()
            return redirect('prueba2')
    return render(request, "home.html", {
        'formset': CompraFormSet
        }
    )