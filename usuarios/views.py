# Django
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Forms
from usuarios.forms import PerfilForm

# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario:
            login(request, usuario)
            return redirect('explicacion')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Usuario y/o Contraseña Invalidos'})
    return render(request, 'usuarios/login.html')


@login_required
def profile_view(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            perfil.celular = data['celular']
            perfil.foto = data['foto']
            perfil.save()
            return redirect('profile')
    else:
        form = PerfilForm()
    return render(
        request=request,
        template_name='usuarios/profile.html',
        context={'perfil': request.user.perfil,
                 'usuario': request.user, 'form': form}
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def explanation_view(request):
    return render(
        request=request,
        template_name='usuarios/explicacion.html',
    )
