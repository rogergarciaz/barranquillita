# Django
from django.contrib import admin

# Models
from sueldos.models import Sueldo
from sueldos.models import Descripcion

# Register your models here.
admin.site.register(Sueldo)
admin.site.register(Descripcion)