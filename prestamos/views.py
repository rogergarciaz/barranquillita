# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from prestamos.forms import PrestamoForm

# Models
from usuarios.models import Perfil
# Create your views here.


@login_required
def create_loan(request):
    usuarios = Perfil.objects.all()
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.agregado = request.user.username
            prestamo.modificado_por = request.user.username
            prestamo.save()
            return redirect('prestamo')
    else:
        form = PrestamoForm()
    return render(request, 'prestamos/prestamo.html', {'usuarios': usuarios})
