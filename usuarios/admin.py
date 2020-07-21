#Django
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import User

#Models
from usuarios.models import Perfil

# Register your models here.
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('pk', 'usuario', 'celular','seguro', 'recordar', 'foto')
    list_display_links = ('pk', 'usuario')
    list_editable = ('celular', 'foto', 'seguro', 'recordar')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name')
    list_filter = ('usuario__is_active', 'usuario__is_staff', 'creado')
    fieldsets = (
        ('Perfil', {
            'fields' : (
                ('usuario', 'foto'),
                ('usuario__first_name', 'usuario__last_name'),
            ),
        }),
        ('Informacion Extra', {
            'fields' : (
                ('celular',),
                ('recordar', 'seguro'),
            ),
        }),
        ('Metadata', {
            'fields' : (('creado', 'modificado'),),
        }),
    )

    readonly_fields = ('creado', 'modificado',)

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfiles'

class UsuarioAdmin(UserAdmin):
    inlines = (PerfilInline,)
    list_display = (
        'username',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
    )

admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)