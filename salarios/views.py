# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from salarios.forms import ProductionForm
from django.contrib.auth.models import User
# Models
from sueldos.models import Descripcion
# Create your views here.
@login_required
def create_production(request):
    usuarios = User.objects.all()
    descripciones = Descripcion.objects.all()
    if request.method == 'POST':
        import pdb; pdb.set_trace()
        form = ProductionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produccion')
    else:
        form = ProductionForm()
    return render(request, 'salarios/produccion.html', {'usuarios':usuarios, 'descripciones':descripciones})