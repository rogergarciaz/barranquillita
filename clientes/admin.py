# Django
from django.contrib import admin

# Models
from clientes.models import Cliente, Compra

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Compra)
