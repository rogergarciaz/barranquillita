# Django
from django.contrib import admin

# Models
from proveedores.models import Proveedor, Adquisicion


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'celular', 'direccion', 'saldo', 'nota', 'ciudad', 'modificado', 'creado')
    list_display_links = ('pk', 'nombre')
    list_editable = ('celular', 'direccion', 'ciudad', 'saldo', 'nota',)
    search_fields = ('nombre','celular', 'direccion', 'nota')
    list_filter = ('nombre', 'ciudad', 'saldo', 'creado', 'modificado')
    fieldsets = (
        ('Proveedor', {
            'fields' : (
                ('nombre', 'celular'),
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

class AdquisicionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'descripcion', 'cantidad', 'precio_compra', 'usuario', 'nota', 'compra', 'modificado', 'creado')
    list_display_links = ('pk', 'nombre')
    list_editable = ('descripcion', 'cantidad', 'precio_compra', 'nota',)
    search_fields = ('nombre', 'usuario', 'descripcion', 'compra', 'nota')
    list_filter = ('nombre', 'usuario', 'descripcion', 'creado', 'modificado')
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
                ('compra','nota')
            ),
        }),
        ('Metadata', {
            'fields' : (('creado', 'modificado'),),
        }),
    )

    readonly_fields = ('creado', 'modificado',)

# Register your models here.
admin.site.register(Proveedor,ProveedorAdmin)
admin.site.register(Adquisicion,AdquisicionAdmin)