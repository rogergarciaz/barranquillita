# Django
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Produccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    perfil = models.ForeignKey(
        'usuarios.Perfil', on_delete=models.CASCADE, default=None)
    descripcion = models.ForeignKey(
        'sueldos.Descripcion', on_delete=models.CASCADE)
    area = models.CharField(max_length=20, blank=False, default=None)
    cantidad = models.FloatField(blank=False)
    precio_pagado = models.FloatField(blank=False)
    nota = models.CharField(max_length=100, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    agregado = models.CharField(max_length=100, blank=False, default=None)
    modificado_por = models.CharField(
        max_length=100, blank=False, default=None)

    def __str__(self):
        return '{} {} produjo {} de {} el {}'.format(
            self.usuario.first_name,
            self.usuario.last_name,
            self.cantidad,
            self.descripcion.nombre,
            self.creado.strftime('%Y-%m-%d')
        )


class ProduccionInterna(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    perfil = models.ForeignKey(
        'usuarios.Perfil', on_delete=models.CASCADE, default=None)
    descripcion = models.ForeignKey(
        'sueldos.DescripcionInterna', on_delete=models.CASCADE)
    area = models.CharField(max_length=20, blank=False, default=None)
    cantidad = models.FloatField(blank=False)
    precio_pagado = models.FloatField(blank=False)
    nota = models.CharField(max_length=100, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    agregado = models.CharField(max_length=100, blank=False, default=None)
    modificado_por = models.CharField(
        max_length=100, blank=False, default=None)
    ingresado = models.BooleanField(blank=False, default=True)

    def __str__(self):
        return '{} {} produjo {} de {} el {}'.format(
            self.usuario.first_name,
            self.usuario.last_name,
            self.cantidad,
            self.descripcion.nombre,
            self.creado.strftime('%Y-%m-%d')
        )


class Fijo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    perfil = models.ForeignKey(
        'usuarios.Perfil', on_delete=models.CASCADE, default=None)
    area = models.CharField(max_length=20, blank=False, default=None)
    precio_pagado = models.FloatField(blank=False)
    nota = models.CharField(max_length=100, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    agregado = models.CharField(max_length=100, blank=False, default=None)
    modificado_por = models.CharField(
        max_length=100, blank=False, default=None)

    def __str__(self):
        return '{} {} hizo {} pesos el {}'.format(
            self.usuario.first_name,
            self.usuario.last_name,
            self.precio_pagado,
            self.creado.strftime('%Y-%m-%d')
        )
