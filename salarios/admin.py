# Django
from django.contrib import admin

# Models
from salarios.models import Produccion
from salarios.models import Fijo

# Register your models here.
admin.site.register(Produccion)
admin.site.register(Fijo)