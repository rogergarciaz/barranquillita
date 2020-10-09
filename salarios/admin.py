# Django
from django.contrib import admin

# Models
from salarios.models import Produccion
from salarios.models import Fijo


class ProduccionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'usuario', 'descripcion', 'cantidad',
                    'precio_pagado', 'area', 'nota', 'agregado', 'creado', 'modificado', 'modificado_por')
    list_display_links = ('pk', 'usuario')
    # list_editable = ('descripcion', 'cantidad', 'nota', 'precio_pagado')
    search_fields = ('usuario__username', 'usuario__first_name',
                     'usuario__last_name', 'nota')
    list_filter = ('descripcion', 'area', 'usuario',
                   'precio_pagado', 'creado', 'modificado')
    fieldsets = (
        ('Produccion', {
            'fields': (
                ('usuario', 'cantidad'),
                ('descripcion', 'precio_pagado'),
            ),
        }),
        ('Informacion Extra', {
            'fields': (
                ('nota',),
                ('area',),
            ),
        }),
        ('Metadata', {
            'fields': (('creado', 'modificado'),),
        }),
    )

    readonly_fields = ('creado', 'modificado',)

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.modificado_por = request.user.username
        instance.save()
        form.save_m2m()
        return instance


class FijoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'usuario', 'precio_pagado', 'area',
                    'nota', 'agregado', 'creado', 'modificado', 'modificado_por')
    list_display_links = ('pk', 'usuario')
    # list_editable = ('nota', 'precio_pagado')
    search_fields = ('usuario__username', 'usuario__first_name',
                     'usuario__last_name', 'nota')
    list_filter = ('area', 'usuario', 'precio_pagado', 'creado', 'modificado')
    fieldsets = (
        ('Fijo', {
            'fields': (
                ('usuario', 'precio_pagado'),
                ('area',),
            ),
        }),
        ('Informacion Extra', {
            'fields': (
                ('nota',),
            ),
        }),
        ('Metadata', {
            'fields': (('creado', 'modificado'),),
        }),
    )

    readonly_fields = ('creado', 'modificado',)

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.modificado_por = request.user.username
        instance.save()
        form.save_m2m()
        return instance


# Register your models here.
admin.site.register(Produccion, ProduccionAdmin)
admin.site.register(Fijo, FijoAdmin)
