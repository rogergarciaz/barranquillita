"""barranquillita URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
    path('asistencia/', salarios_views.create_assistance, name='asistencia'),
    path('prestamos/', prestamos_views.create_loan, name='prestamo'),
    path('sueldos/', sueldos_views.create_payment, name='nomina'),
    path('sueldos/nomina/<int:nomina>/', sueldos_views.see_payment, name='nominas'),
    path('sueldos/buscar/', sueldos_views.search_descriptions, name='search'),
    path('clientes/venta', clientes_views.create_sale, name='venta'),
    path('clientes/ventas', clientes_views.create_sale_model_form, name='ventas'),
    path('clientes/factura/<int:factura>/', clientes_views.create_bill, name='facturav'),
    path('proveedores/compra', proveedores_views.create_adquisition, name='compra'),
    path('proveedores/compras', proveedores_views.create_adquisition_model_form, name='compras'),
    path('proveedores/factura/<int:factura>/', proveedores_views.create_bill, name='facturac'),
    path('prueba/', sueldos_views.NominaPDF.as_view(), name='prueba'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
