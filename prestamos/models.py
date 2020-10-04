from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Prestamo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    perfil = models.ForeignKey(
        'usuarios.Perfil', on_delete=models.CASCADE, default=None)
    descripcion = models.CharField(max_length=50, blank=False)
    cuotas = models.PositiveIntegerField(blank=False)
    cuotas_debidas = models.PositiveIntegerField(blank=False)
    valor = models.PositiveIntegerField(blank=False)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    nota = models.CharField(max_length=100, blank=True)
    agregado = models.CharField(max_length=100, blank=False, default=None)

    def __str__(self):
        valor = self.valor/self.cuotas
        debe = valor*self.cuotas_debidas
        return '{} {} debe {} de {} se creo el {}'.format(
            self.usuario.first_name,
            self.usuario.last_name,
            debe,
            self.descripcion,
            self.creado.strftime('%Y-%m-%d %H:%M')
        )
