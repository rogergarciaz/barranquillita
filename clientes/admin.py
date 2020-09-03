# Django
from django.contrib import admin

# Models
from clientes.models import Cliente, Compra


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'celular', 'direccion', 'nota', 'ciudad', 'modificado', 'creado')
    list_display_links = ('pk', 'nombre')
    list_editable = ('celular', 'direccion', 'ciudad', 'nota',)
    search_fields = ('nombre','celular', 'direccion', 'nota')
    list_filter = ('nombre', 'ciudad', 'creado', 'modificado')
    fieldsets = (
        ('Cliente', {
            'fields' : (
                ('nombre', 'celular'),
                ('direccion', 'ciudad'),
            ),
        }),
        ('Informacion Extra', {
            'fields' : (
                ('nota',),
            ),
        }),
        ('Metadata', {
            'fields' : (('creado', 'modificado'),),
        }),
    )

    readonly_fields = ('creado', 'modificado',)

class CompraAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'descripcion', 'cantidad', 'precio_vendido', 'usuario', 'nota', 'venta', 'modificado', 'creado')
    list_display_links = ('pk', 'nombre')
    list_editable = ('descripcion', 'cantidad', 'precio_vendido', 'nota',)
    search_fields = ('nombre', 'usuario', 'descripcion', 'venta', 'nota')
    list_filter = ('nombre', 'usuario', 'descripcion', 'creado', 'modificado')
    fieldsets = (
        ('Compra', {
            'fields' : (
                ('nombre', 'descripcion'),
                ('cantidad', 'precio_vendido'),
            ),
        }),
        ('Informacion Extra', {
            'fields' : (
                ('usuario','nota'),
                ('venta',)
            ),
        }),
        ('Metadata', {
            'fields' : (('creado', 'modificado'),),
        }),
    )

    readonly_fields = ('creado', 'modificado',)

# Register your models here.
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Compra,CompraAdmin)
