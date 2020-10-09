# Django
from django.contrib import admin

# Models
from clientes.models import Cliente, Compra


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'identificador', 'celular', 'direccion', 'saldo', 'nota', 'ciudad', 'creado', 'modificado', 'modificado_por')
    list_display_links = ('pk', 'nombre')
    # list_editable = ('celular', 'direccion', 'saldo', 'ciudad', 'nota',)
    search_fields = ('nombre', 'identificador', 'celular', 'direccion', 'nota')
    list_filter = ('nombre', 'saldo', 'ciudad', 'creado', 'modificado')
    fieldsets = (
        ('Cliente', {
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

class CompraAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'descripcion', 'cantidad', 'credito', 'precio_vendido', 'usuario', 'creado', 'nota', 'venta', 'modificado', 'modificado_por')
    list_display_links = ('pk', 'nombre')
    # list_editable = ('descripcion', 'cantidad', 'precio_vendido', 'nota',)
    search_fields = ('nombre', 'usuario', 'descripcion', 'venta', 'nota')
    list_filter = ('nombre', 'credito', 'usuario', 'descripcion', 'creado', 'modificado')
    fieldsets = (
        ('Compra', {
            'fields' : (
                ('nombre', 'descripcion'),
                ('cantidad', 'precio_vendido'),
            ),
        }),
        ('Informacion Extra', {
            'fields' : (
                ('usuario','perfil'),
                ('venta', 'credito', 'nota')
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
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Compra,CompraAdmin)
