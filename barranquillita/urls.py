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

# Models
from usuarios import views as usuarios_views
from salarios import views as salarios_views
from prestamos import views as prestamos_views
from sueldos import views as sueldos_views
from ventas import views as ventas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/login/', usuarios_views.login_view, name='login'),
    path('usuarios/logout/', usuarios_views.logout_view, name='logout'),
    path('usuarios/', usuarios_views.profile_view, name='profile'),
    path('salarios/produccion/', salarios_views.create_production, name='produccion'),
    path('salarios/fijo/', salarios_views.create_assistance, name='asistencia'),
    path('prestamos/', prestamos_views.create_loan, name='prestamo'),
    path('sueldos/', sueldos_views.create_payment, name='nomina'),
    path('ventas/', ventas_views.create_sale, name='venta'),
    path('prueba/', sueldos_views.NominaPDF.as_view(), name='prueba'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
