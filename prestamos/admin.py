# Django
from django.contrib import admin

# Models
from prestamos.models import Prestamo


class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'usuario', 'perfil', 'descripcion', 'valor', 'cuotas',
                    'cuotas_debidas', 'nota', 'agregado', 'creado', 'modificado', 'modificado_por')
    list_display_links = ('pk', 'usuario')
    # list_editable = ('nota', 'valor', 'cuotas', 'cuotas_debidas')
    search_fields = ('usuario__username', 'usuario__first_name',
                     'usuario__last_name', 'nota')
    list_filter = ('descripcion', 'cuotas_debidas',
                   'usuario', 'creado', 'modificado')
    fieldsets = (
        ('Prestamo', {
            'fields': (
                ('usuario', 'perfil',),
                ('descripcion',),
                ('valor', 'agregado'),
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

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.modificado_por = request.user.username
        instance.save()
        form.save_m2m()
        return instance


# Register your models here.
admin.site.register(Prestamo, PrestamoAdmin)
