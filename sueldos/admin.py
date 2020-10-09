# Django
from django.contrib import admin

# Models
from sueldos.models import Sueldo
from sueldos.models import Descripcion


class SueldoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'usuario', 'valor', 'nota', 'sueldo',
                    'agregado', 'creado', 'modificado', 'modificado_por')
    list_display_links = ('pk', 'usuario')
    # list_editable = ('valor', 'nota', 'sueldo')
    search_fields = ('usuario__username', 'usuario__first_name',
                     'usuario__last_name', 'nota')
    list_filter = ('usuario', 'sueldo', 'valor', 'modificado', 'creado')
    fieldsets = (
        ('Sueldo', {
            'fields': (
                ('usuario', 'valor'),
            ),
        }),
        ('Informacion Extra', {
            'fields': (
                ('nota',),
                ('sueldo', 'agregado', ),
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


class DescripcionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'precio_vendido', 'precio_pagado',
                    'precio_compra', 'cantidad', 'area', 'modificado', 'modificado_por', 'creado')
    list_display_links = ('pk',)
    # list_editable = ('nombre', 'precio_vendido', 'area',
    #                  'precio_pagado', 'precio_compra', 'cantidad')
    search_fields = ('nombre', 'precio_vendido',
                     'precio_pagado', 'precio_compra', 'cantidad')
    list_filter = ('nombre', 'precio_vendido', 'precio_pagado',
                   'precio_compra', 'cantidad', 'modificado', 'creado')
    fieldsets = (
        ('Descripcion', {
            'fields': (
                ('nombre', 'cantidad'),
                ('area', ),
            ),
        }),
        ('Informacion Extra', {
            'fields': (
                ('precio_vendido', 'precio_pagado', 'precio_compra'),
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
admin.site.register(Sueldo, SueldoAdmin)
admin.site.register(Descripcion, DescripcionAdmin)
