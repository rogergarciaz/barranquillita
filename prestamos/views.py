#Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from prestamos.forms import PrestamoForm
from django.contrib.auth.models import User


# Create your views here.
@login_required
def create_loan(request):
    usuarios = User.objects.all()
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prestamo')
    else:
        form = PrestamoForm()
    return render(request, 'prestamos/prestamo.html', {'usuarios':usuarios})