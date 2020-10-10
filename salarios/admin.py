# Django
from django.contrib import admin

# Models
from salarios.models import Produccion, Fijo, ProduccionInterna


class ProduccionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'usuario', 'descripcion', 'cantidad', 'agregado', 'perfil',
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
                ('perfil', 'agregado'),
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


class ProduccionInternaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'usuario', 'descripcion', 'cantidad', 'perfil', 'agregado',
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
                ('perfil', 'agregado'),
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
    list_display = ('pk', 'usuario', 'precio_pagado', 'area', 'perfil', 'agregado',
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
                ('area', 'perfil'),
            ),
        }),
        ('Informacion Extra', {
            'fields': (
                ('nota', 'agregado'),
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
admin.site.register(ProduccionInterna, ProduccionInternaAdmin)
admin.site.register(Fijo, FijoAdmin)
