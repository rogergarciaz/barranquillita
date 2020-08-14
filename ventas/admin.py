# Django
from django.contrib import admin

# Models
from ventas.models import Venta, Cliente

# Register your models here.
admin.site.register(Venta)
admin.site.register(Cliente)