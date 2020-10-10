"""barranquillita URL Configuration
"""
# Django
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# Views
from usuarios import views as usuarios_views
from salarios import views as salarios_views
from prestamos import views as prestamos_views
from sueldos import views as sueldos_views
from clientes import views as clientes_views
from proveedores import views as proveedores_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usuarios_views.login_view, name='login'),
    path('logout/', usuarios_views.logout_view, name='logout'),
    path('usuarios/', usuarios_views.profile_view, name='profile'),
    path('produccion/', salarios_views.create_production, name='produccion'),
    path('sacado/', salarios_views.take_production, name='sacado'),
    path('producto/', salarios_views.create_product, name='producto'),
    path('asistencia/', salarios_views.create_assistance, name='asistencia'),
    path('prestamos/', prestamos_views.create_loan, name='prestamo'),
    path('sueldos/', sueldos_views.create_payment, name='nomina'),
    path('sueldos/nomina/<int:nomina>/',
         sueldos_views.see_payment, name='nominas'),
    path('sueldos/productos/', sueldos_views.search_descriptions, name='buscar'),
    path('sueldos/produccion/',
         sueldos_views.search_internal_descriptions, name='buscarP'),
    path('clientes/ventas', clientes_views.create_sale_model_form, name='ventas'),
    path('clientes/factura/<int:factura>/',
         clientes_views.create_bill, name='facturav'),
    path('clientes/acumulado', clientes_views.see_consolidate, name='acumulado'),
    path('clientes/acumulados',
         clientes_views.see_consolidateDates, name='acumuladoF'),
    path('proveedores/compras',
         proveedores_views.create_adquisition_model_form, name='compras'),
    path('proveedores/factura/<int:factura>/',
         proveedores_views.create_bill, name='facturac'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
