from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=100, blank=False, default=None)
    seguro = models.PositiveIntegerField()
    recordar = models.PositiveIntegerField()
    celular = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='usuarios/fotos', blank=True, null=True)
    nacimiento = models.DateField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    modificado_por = models.CharField(max_length=100, blank=False, default=None)

    def __str__(self):
        return '{} {} - {}'.format(
            self.usuario.first_name,
            self.usuario.last_name,
            self.identificador
        )