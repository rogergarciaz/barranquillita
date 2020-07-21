from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Prestamo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    perfil = models.ForeignKey('usuarios.Perfil', on_delete=models.CASCADE, default=None)
    descripcion = models.CharField(max_length=50, blank=False)
    cuotas = models.PositiveIntegerField(blank=False)
    cuotas_pagadas = models.PositiveIntegerField(blank=False)
    valor = models.PositiveIntegerField(blank=False)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        cantidad = self.cuotas - self.cuotas_pagadas
        valor = self.valor/self.cuotas
        debe = valor*cantidad
        return '{} {} debe {} de {}'.format(
            self.usuario.first_name,
            self.usuario.last_name,
            debe,
            self.descripcion
        )