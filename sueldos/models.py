from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Sueldo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    perfil = models.ForeignKey('usuarios.Perfil', on_delete=models.CASCADE, default=None)
    nota = models.CharField(max_length=100, blank=True)
    sueldo = models.PositiveIntegerField(blank=False)
    valor = models.PositiveIntegerField(blank=False)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'El sueldo de {} {} es de {} pesos'.format(
            self.usuario.first_name,
            self.usuario.last_name,
            self.valor
        )

class Descripcion(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.nombre)