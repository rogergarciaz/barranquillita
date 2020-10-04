# Django
from django.contrib import admin

# Models
from prestamos.models import Prestamo


class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'usuario', 'perfil', 'descripcion', 'valor', 'cuotas',
                    'cuotas_debidas', 'nota', 'agregado', 'modificado', 'creado')
    list_display_links = ('pk', 'usuario')
    list_editable = ('nota', 'valor', 'cuotas', 'cuotas_debidas')
    search_fields = ('usuario__username', 'usuario__first_name',
                     'usuario__last_name', 'nota')
    list_filter = ('descripcion', 'cuotas_debidas',
                   'usuario', 'creado', 'modificado')
    fieldsets = (
        ('Prestamo', {
            'fields': (
                ('usuario', 'perfil',),
                ('descripcion',),
                ('valor', 'agregado',),
            ),
        }),
        ('Informacion Extra', {
            'fields': (
                ('nota',),
                ('cuotas', 'cuotas_debidas'),
            ),
        }),
        ('Metadata', {
            'fields': (('creado', 'modificado'),),
        }),
    )

    readonly_fields = ('creado', 'modificado',)


# Register your models here.
admin.site.register(Prestamo, PrestamoAdmin)
