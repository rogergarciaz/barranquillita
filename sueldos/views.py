import pytz
import io
import datetime
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from prestamos.forms import PrestamoForm
from django.db.models import F
from django.http import FileResponse
from django.utils import timezone
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from django.forms.models import model_to_dict
from django.views.generic import TemplateView, ListView
from django.db.models import Q

# Models
from sueldos.models import Sueldo, Descripcion
from salarios.models import Produccion, Fijo
from prestamos.models import Prestamo
from usuarios.models import Perfil


# Create your views here

# class NominaPDF(View):
#     def cabecera(self, pdf):
#         # Fechas
#         nomina_actual = Sueldo.objects.last()
#         nomina_antigua = Sueldo.objects.filter(
#             sueldo=nomina_actual.sueldo - 1
#         ).order_by('-id')[0]
#         self.fechaI = nomina_antigua.creado + datetime.timedelta(seconds=3)
#         self.fechaF = nomina_actual.creado
#         desde = 'Del ' + \
#             self.fechaI.strftime("%Y-%m-%d") + ' al ' + \
#             self.fechaF.strftime("%Y-%m-%d")
#         namefile = 'Nomina ' + self.fechaF.strftime("%Y-%m-%d") + '.pdf'
#         pdf.setTitle(namefile)
#         # Utilizamos el archivo pupiplast guardado en static
#         archivo_imagen = settings.MEDIA_FILES+'pupiplast.png'
#         # ( "x" grandes es derecha - "y" grandes es arriba ) #
#         # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
#         pdf.drawImage(archivo_imagen, 15, 730, 120, 90, mask=[
#                       0, 0, 0, 0, 0, 0], preserveAspectRatio=True)
#         # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
#         pdf.setFont("Helvetica", 16)
#         # Dibujamos una cadena en la ubicación X,Y especificada
#         pdf.drawString(230, 790, "Barranquillita Nomina")
#         pdf.setFont("Helvetica", 14)
#         pdf.drawString(215, 770, desde)

#     def tabla(self, pdf, width, height):
#         # Creamos una tupla de encabezados para neustra tabla
#         encabezados = ('#', 'Nomina', 'Nombres', 'Apellidos', 'Sueldo', 'Nota')
#         # Creamos una lista de tuplas que van a contener a las personas
#         detalles = [(
#             sueldo.pk, sueldo.sueldo, sueldo.usuario.first_name,
#             sueldo.usuario.last_name, sueldo.valor, sueldo.nota
#         )
#             for sueldo in Sueldo.objects.filter(creado__range=[self.fechaI, self.fechaF])
#         ]
#         # detalles = [(
#         #     sueldo.pk, sueldo.sueldo, sueldo.usuario.first_name,
#         #     sueldo.usuario.last_name, sueldo.valor, sueldo.nota
#         #     )
#         #     for sueldo in Sueldo.objects.all()
#         # ]
#         # Establecemos el tamaño de cada una de las columnas de la tabla
#         detalle_orden = Table(
#             [encabezados] + detalles,
#             colWidths=[1 * cm, 2 * cm, 2 * cm, 3 * cm, 2 * cm, 3 * cm]
#         )
#         # Aplicamos estilos a las celdas de la tabla
#         detalle_orden.setStyle(TableStyle(
#             [
#                 # ('Property', (Xi,Yi), (Xf,Yf), Color)
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.green),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                 ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
#                 ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#                 # La primera fila(encabezados) va a estar centrada
#                 ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#                 ('ALIGN', (0, 0), (1, -1), 'CENTER'),
#                 # Los bordes de todas las celdas serán de color negro y con un grosor de 1
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
#                 # El tamaño de las letras de cada una de las celdas será de 10
#                 ('FONTSIZE', (0, 0), (-1, -1), 10),
#             ]
#         ))
#         # Establecemos el tamaño de la hoja que ocupará la tabla
#         detalle_orden.wrapOn(pdf, width, height)
#         # Definimos la coordenada donde se dibujará la tabla
#         detalle_orden.drawOn(pdf, 4 * cm, 12 * cm)

#     def get(self, request, *args, **kwargs):
#         width, height = A4
#         # Indicamos el tipo de contenido a devolver, en este caso un pdf
#         response = HttpResponse(content_type='application/pdf')
#         # La clase io.BytesIO permite tratar un array de bytes como un fichero binario,
#         # se utiliza como almacenamiento temporal
#         buffer = io.BytesIO()
#         # Canvas nos permite hacer el reporte con coordenadas X y Y
#         pdf = canvas.Canvas(buffer, pagesize=A4)
#         # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte
#         self.cabecera(pdf)
#         self.tabla(pdf, width, height)
#         # Con showPage hacemos un corte de página para pasar a la siguiente
#         pdf.showPage()
#         pdf.save()
#         pdf = buffer.getvalue()
#         buffer.close()
#         response.write(pdf)
#         return response

def sacar_sueldo(perfil, fechaI, fechaF, ver):
    valorP = 0
    valorF = 0
    valorD = 0
    # Agregando produccion
    producido = Produccion.objects.filter(
        usuario=perfil.usuario,
        creado__range=[fechaI, fechaF]
    )
    for produccion in producido:
        valorP = valorP + produccion.precio_pagado * produccion.cantidad
    # Agregando por dia
    fijos = Fijo.objects.filter(
        usuario=perfil.usuario,
        creado__range=[fechaI, fechaF]
    )
    for fijo in fijos:
        valorF = valorF + fijo.precio_pagado
    # Agregando prestamos
    prestamos = Prestamo.objects.filter(
        usuario=perfil.usuario,
        cuotas_debidas__gt=0,
    )
    for prestamo in prestamos:
        valorD = valorD + prestamo.valor/prestamo.cuotas
    if prestamos and ver:
        prestamos.update(cuotas_debidas=F('cuotas_debidas') - 1)
    # Valor Total
    valor = valorP + valorF - valorD - perfil.seguro - perfil.recordar
    return valor, valorP, valorF, valorD


@login_required
def create_payment(request):
    # if request.user.is_staff:
    nomina_antigua = Sueldo.objects.last()
    fechaI = nomina_antigua.creado
    if request.method == 'POST':
        ver = True  # disminuye cuotas de prestamos
        fechaF = datetime.datetime.now()  # not include day of click
        sueldo = nomina_antigua.sueldo + 1
        perfiles = Perfil.objects.filter(usuario__is_active=True)
        for perfil in perfiles:
            valor, valorP, valorF, valorD = sacar_sueldo(
                perfil, fechaI, fechaF, ver)
            nomina = Sueldo(
                usuario=perfil.usuario,
                perfil=perfil,
                nota=request.POST['nota'],
                sueldo=sueldo,
                valor=valor,
                agregado=request.user.username
            )
            nomina.save()
        return redirect('nominas', nomina=sueldo)
    return render(request, 'sueldos/nomina.html')


@login_required
def see_payment(request, nomina):
    # if request.user.is_staff:
    ver = False  # no disminuye cuotas de prestamos
    sueldos = Sueldo.objects.filter(sueldo=nomina)
    fechaI = Sueldo.objects.filter(
        sueldo=nomina-1).last().creado + datetime.timedelta(seconds=3)
    fechaF = sueldos.last().creado + datetime.timedelta(seconds=3)
    subtotal = []
    conteo = 1
    total = 0
    for sueldo in sueldos:
        copia = model_to_dict(sueldo).copy()
        valor, valorP, valorF, valorD = sacar_sueldo(
            sueldo.perfil, fechaI, fechaF, ver)
        copia['empleado'] = str(sueldo.perfil.usuario.get_full_name())
        copia['valor'] = valor
        copia['valorP'] = valorP
        copia['valorF'] = valorF
        copia['valorD'] = valorD
        copia['numero'] = conteo
        subtotal.append(copia)
        conteo += 1
        total = total + valor
    return render(request, "sueldos/sueldo.html", {
        'sueldos': subtotal,
        'nomina': nomina,
        'total': total,
    }
    )


def search_descriptions(request):
    descripciones = Descripcion.objects.filter(cantidad__lte=500)
    query = "Escribe la descripción"
    if request.method == 'POST':
        query = request.POST['description']
        if query.isnumeric():
            descripciones = Descripcion.objects.filter(
                Q(cantidad=query)
            )
        else:
            descripciones = Descripcion.objects.filter(
                Q(nombre__icontains=query)
            )
        return render(request, "sueldos/buscar.html", {
            'descripciones': descripciones,
            'query': query,
        }
        )
    return render(request, "sueldos/buscar.html", {
        'descripciones': descripciones,
        'query': query,
    }
    )
