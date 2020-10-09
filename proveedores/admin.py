# Django
from django.contrib import admin

# Models
from proveedores.models import Proveedor, Adquisicion


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'identificador', 'celular', 'direccion', 'saldo', 'nota', 'ciudad', 'creado', 'modificado', 'modificado_por')
    list_display_links = ('pk', 'nombre')
    # list_editable = ('celular', 'direccion', 'ciudad', 'saldo', 'nota',)
    search_fields = ('nombre', 'identificador', 'celular', 'direccion', 'nota')
    list_filter = ('nombre', 'ciudad', 'saldo', 'creado', 'modificado')
    fieldsets = (
        ('Proveedor', {
            'fields' : (
                ('nombre', 'identificador', 'celular'),
                ('direccion', 'ciudad'),
            ),
        }),
        ('Informacion Extra', {
            'fields' : (
                ('nota', 'saldo',),
            ),
        }),
        ('Metadata', {
            'fields' : (('creado', 'modificado'),),
        }),
    )

    readonly_fields = ('creado', 'modificado',)

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.modificado_por = request.user.username
        instance.save()
        form.save_m2m()
        return instance

class AdquisicionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'descripcion', 'credito', 'cantidad', 'precio_compra', 'usuario', 'nota', 'compra', 'creado', 'modificado', 'modificado_por')
    list_display_links = ('pk', 'nombre')
    # list_editable = ('descripcion', 'cantidad', 'precio_compra', 'nota',)
    search_fields = ('nombre', 'usuario', 'descripcion', 'compra', 'nota')
    list_filter = ('nombre', 'credito', 'usuario', 'descripcion', 'creado', 'modificado')
    fieldsets = (
        ('Adquisicion', {
            'fields' : (
                ('nombre', 'descripcion'),
                ('cantidad', 'precio_compra'),
            ),
        }),
        ('Informacion Extra', {
            'fields' : (
                ('usuario', 'perfil'),
                ('compra', 'credito', 'nota')
            ),
        }),
        ('Metadata', {
            'fields' : (('creado', 'modificado'),),
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
admin.site.register(Proveedor,ProveedorAdmin)
admin.site.register(Adquisicion,AdquisicionAdmin)