from io import BytesIO
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from datetime import timedelta

import qrcode

from inventario.views import is_in_allowed_groups
from inventario.models import Equipo
from metrologia.models import ControlMetro, DetalleControlMetro
from .models import EspecificacionVerificacion, Verificacion
from .forms import ModificarEspForm, RegistrarEspVerForm, VerificacionForm



from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from django.conf import settings
 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
 
# Obtener estilos de ejemplo
estilos = getSampleStyleSheet()
 
# Crear un estilo personalizado
estilo_normal1 = ParagraphStyle(
    'estilo_personalizado1',
    parent=estilos['Normal'],
    fontSize=13,
    textColor='black',
    alignment=1,  # 0: Izquierda, 1: Centro, 2: Derecha
)
 
# Crear un estilo personalizado
estilo_normal2 = ParagraphStyle(
    'estilo_personalizado2',
    parent=estilos['Normal'],
    fontSize=11,
    textColor='black',
    alignment=0,  # 0: Izquierda, 1: Centro, 2: Derecha
)
 
# Crear un estilo personalizado
estilo_subTitulo1 = ParagraphStyle(
    'estilo_personalizado2',
    parent=estilos['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    textColor='black',
    alignment=2,  # 0: Izquierda, 1: Centro, 2: Derecha
)
 
# Definir estilo personalizado para el texto
estilo_titulo = estilos['Title']
estilo_normal = estilos['Normal']
estilo_texto = estilos['BodyText']
 
 
def generar_pdf(request, id ,pk, error):
    verificacion = get_object_or_404(Verificacion, num_informe=pk)
    esp_verificacion = get_object_or_404(EspecificacionVerificacion, id_equipo=verificacion.id_verificacion)


    # Obtener la fecha actual en el formato deseado (DD / MM / YYYY)
    fecha_actual = datetime.now().strftime("%d / %m / %Y")
 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename= "Reporte de verificación_{verificacion.num_informe}_{verificacion.fecha}.pdf"'
 
    # Crear el objeto PDF usando ReportLab
    p = SimpleDocTemplate(response, pagesize=letter)
 
 
 
    # Crea la URL para el código QR (ajusta la URL según tus necesidades)
    qr_url = f"http://127.0.0.1:8000/verificacion/detalles/{verificacion.num_informe}/"
 
    # Crea el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
 
    # Crea una imagen del código QR
    img_QR = qr.make_image(fill_color="black", back_color="white")
 
    # Guarda la imagen del código QR
    buffer = BytesIO()
    img_QR.save(buffer, format="PNG")
 
    image_QR = (Image(buffer, width=125, height=125))

 
 
    # Agregar espaciador para crear un salto de línea
    espaciador = Spacer(1, 12)
 
    # Estilos de texto
    estilo_normal.alignment = 2
 
    color_rgb = tuple(int(x, 16) / 255.0 for x in ('7B', '2D', '26'))
 
    # Datos para la tabla
    datos_tabla_fecha = [
        ['Fecha de verificación', 'Periodo entre verificaciones', 'Fecha de próxima verificación'],
        [f'{esp_verificacion.ultima}', f'{esp_verificacion.periodo} mes(es)', f'{esp_verificacion.proxima}'],
    ]
 
    # Crear la tabla
    tabla_fecha = Table(datos_tabla_fecha)
 
    # Establecer estilos para la tabla
    estilo_tabla_fecha = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), color_rgb),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agrega bordes negros a la tabla
    ])
 
    # Aplicar estilos a la tabla
    tabla_fecha.setStyle(estilo_tabla_fecha)
 


    # Datos para la tabla
    datos_tabla_detalles_verificacion = [
        ['Punto de verificación', 'Unidad', 'Lectura equipo', 'Lectura patrón', 'Error'],
        [f'{verificacion.puntoVer1}', f'{error}', f'{verificacion.lecEq1}', f'{verificacion.lecPatron1}', f'{verificacion.errorVer1}'],
        [f'{verificacion.puntoVer2}', f'{error}', f'{verificacion.lecEq2}', f'{verificacion.lecPatron2}', f'{verificacion.errorVer2}'],
        [f'{verificacion.puntoVer3}', f'{error}', f'{verificacion.lecEq3}', f'{verificacion.lecPatron3}', f'{verificacion.errorVer3}'],
        [f'{verificacion.puntoVer4}', f'{error}', f'{verificacion.lecEq4}', f'{verificacion.lecPatron4}', f'{verificacion.errorVer4}'],
        [f'{verificacion.puntoVer5}', f'{error}', f'{verificacion.lecEq5}', f'{verificacion.lecPatron5}', f'{verificacion.errorVer5}'],
    ]
 
    # Crear la tabla
    tabla_detalles_verificacion = Table(datos_tabla_detalles_verificacion)
 
    # Establecer estilos para la tabla
    estilo_tabla_detalles_verificacion = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), color_rgb),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agrega bordes negros a la tabla
    ])
 
    # Aplicar estilos a la tabla
    tabla_detalles_verificacion.setStyle(estilo_tabla_detalles_verificacion)

 
 
# Datos para la tabla
    datos_tabla_dictamen = [
        ['Confirmación metrológica'],
        [f'{verificacion.dictamen}'],
    ]
 
    # Crear la tabla
    tabla_dictamen = Table(datos_tabla_dictamen)
 
    # Establecer estilos para la tabla de dictamen
    estilo_tabla_dictamen = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), color_rgb),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agrega bordes negros a la tabla
 
        ('LEFTPADDING', (0, 0), (-1, 0), 10),
        ('RIGHTPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
 
        ('LEFTPADDING', (0, 1), (-1, -1), 8),
        ('RIGHTPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ])
 
    # Aplicar estilos a la tabla
    tabla_dictamen.setStyle(estilo_tabla_dictamen)
 
 
    # Ruta a tu imagen
    ruta_imagen1 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/logo_ciateq.png'
 
    # Crear el objeto de la imagen
    imagen1 = Image(ruta_imagen1, width=90, height=77)
    imagen1.hAlign = 'LEFT'
    imagen1.vAlign = 'TOP'

 
    # Ruta a tu imagen
    ruta_imagen_subtitle1 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/ico_calendar1.png'
 
    # Crear el objeto de la imagen
    imagen_subtitle1 = Image(ruta_imagen_subtitle1, width=18, height=18)
    imagen_subtitle1.vAlign = 'BOTTOM'
 
 
    # Ruta a tu imagen
    ruta_imagen_subtitle2 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/ico_EspecificacionMetrologica.png'
 
    # Crear el objeto de la imagen
    imagen_subtitle2 = Image(ruta_imagen_subtitle2, width=18, height=18)
    imagen_subtitle2.vAlign = 'BOTTOM'
 
 
    # Crear el objeto de fecha de captura
    fecha_captura = Paragraph(f"Fecha de captura: {fecha_actual}", estilo_subTitulo1)
 
 
    # Organizar elementos en dos columnas
    columna_izquierda = [
        ['Folio:', verificacion.num_informe],
        ['Proveedor de verificación:', verificacion.id_responsable],
        ['Patrón utilizado:', verificacion.id_patron],
        ['Aprobo:', verificacion.id_aprobación],
        [espaciador, espaciador],
 
    ]
 
    columna_derecha = [
        [image_QR],
    ]
 
    # Establecer estilos para la tabla izquierda
    estilo_tabla_izquierda = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Alinea la primera columna a la izquierda
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Alinea la segunda columna al centro
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Ajusta el espacio entre las filas
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ])
 
    # Establecer estilos para la tabla
    estilo_tabla_derecha = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ])
 
    # Crear tablas para cada columna
    tabla_izquierda = Table(columna_izquierda, colWidths='*')
    tabla_derecha = Table(columna_derecha, colWidths='*')
 
    # Aplicar estilos a las tablas
    tabla_izquierda.setStyle(estilo_tabla_izquierda)
    tabla_derecha.setStyle(estilo_tabla_derecha)
 
    # Organizar ambas tablas en una tabla principal
    tabla_principal_data = [
        [tabla_izquierda, tabla_derecha],
    ]
 
    tabla_principal = Table(tabla_principal_data, colWidths=[325, 140])  # Ajusta el ancho de las columnas según sea necesario
 
 
 
 
 
# Organizar elementos en dos columnas
 
    columna_izquierda1 = [
        [imagen1],
    ]
 
    columna_derecha1 = [
        ['Reporte de verificación'],
        [f'Equipo: {verificacion.id_verificacion}'],
        [Spacer(1,4)],
    ]
 
   
 
    # Establecer estilos para la tabla izquierda
    estilo_tabla_derecha1 = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Alinea la primera columna a la izquierda
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Alinea la segunda columna al centro
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 18),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 13),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 13),  # Ajusta el espacio entre las filas
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ])
 
    # Establecer estilos para la tabla
    estilo_tabla_izquierda1 = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ])
 
    # Crear tablas para cada columna
    tabla_izquierda1 = Table(columna_izquierda1, colWidths='*')
    tabla_derecha1 = Table(columna_derecha1, colWidths='*')
 
    # Aplicar estilos a las tablas
    tabla_izquierda1.setStyle(estilo_tabla_izquierda1)
    tabla_derecha1.setStyle(estilo_tabla_derecha1)
 
    # Organizar ambas tablas en una tabla principal
    tabla_principal_data1 = [
        [tabla_izquierda1, tabla_derecha1],
    ]
 
    tabla_principal1 = Table(tabla_principal_data1, colWidths=[125, 340])  # Ajusta el ancho de las columnas según sea necesario
 
 
 
 
 
 
    # Datos para la tabla
    datos_tabla_subtitle1 = [
        [imagen_subtitle1, 'Fechas de verificación'],
    ]
 
    # Crear la tabla
    tabla_subtitle1 = Table(datos_tabla_subtitle1)
 
    # Establecer estilos para la tabla
    estilo_tabla_subtitle1 = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
    ])
 
    # Aplicar estilos a la tabla
    tabla_subtitle1.setStyle(estilo_tabla_subtitle1)
    tabla_subtitle1.hAlign = 0
 
 
 
 
    # Datos para la tabla
    datos_tabla_subtitle2 = [
        [imagen_subtitle2, 'Detalles de verificación'],
    ]
 
    # Crear la tabla
    tabla_subtitle2 = Table(datos_tabla_subtitle2)
 
    # Establecer estilos para la tabla
    estilo_tabla_subtitle2 = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
    ])
 
    # Aplicar estilos a la tabla
    tabla_subtitle2.setStyle(estilo_tabla_subtitle2)
    tabla_subtitle2.hAlign = 0
 
 
 
 
    # Datos para la tabla
    datos_tabla_captura = [
        [f'Responsable de captura: {verificacion.id_responsable}', f'Fecha de impresión: {fecha_actual}'],
    ]
 
    # Crear la tabla
    tabla_captura = Table(datos_tabla_captura, colWidths=[450, 40])
 
    # Establecer estilos para la tabla
    estilo_tabla_captura = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Alinea la primera columna a la izquierda
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),  # Alinea la segunda columna a la derecha
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
    ])
 
    # Aplicar estilos a la tabla
    tabla_captura.setStyle(estilo_tabla_captura)
    tabla_captura.hAlign = 1
 
 
 
 
    # Agregar elementos al PDF
    elementos = [
                fecha_captura, espaciador, tabla_principal1, tabla_principal,
                tabla_subtitle1, Spacer(1, 10), tabla_fecha,
                Spacer(1, 20), tabla_subtitle2, Spacer(1, 10),
                ]
 
 
    # Agregar la tabla de criterios a los elementos
    elementos.append(tabla_detalles_verificacion)
    elementos.append(Spacer(1, 20))
    elementos.append(tabla_dictamen)
    elementos.append(Spacer(1, 11))
    elementos.append(tabla_captura)
 
    p.build(elementos)
 
    # Devuelve la respuesta generada por la función
    return response
 
 
 




@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class ModificarEspView(generic.UpdateView):
    model = EspecificacionVerificacion
    form_class = ModificarEspForm
    template_name = 'verificacion/modificarEspVer.html'  

    def get_success_url(self):
        return reverse('verificacion:verificacion')


class VerificacionView(LoginRequiredMixin, generic.ListView):
    template_name = "verificacion/verificacion.html"
    context_object_name = "all_items"

    def get_queryset(self):
        return EspecificacionVerificacion.objects.all()
    
class DetallesVerView(LoginRequiredMixin, generic.DetailView):
    model = Verificacion
    template_name = "verificacion/detallesVerificacion.html"
    context_object_name = 'verificacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = str(self.object.id_verificacion)
        equipo = Equipo.objects.get(id=pk)
        unidad_error = DetalleControlMetro.objects.filter(id_controlMetro=pk, id_criterio="Error").first().id_unidad_criterio
        img_eq = equipo.imagen
        context['unidad_error'] = unidad_error
        if img_eq :
            context['img_eq'] = img_eq.url
        else:
            context['img_eq'] = "/media/imgs/img/ico_noImage1.png"
        return context

@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class AgregarEspVerView(generic.CreateView):
    model = EspecificacionVerificacion
    form_class = RegistrarEspVerForm
    template_name = 'verificacion/especificacionVerificacion.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_equipo = self.kwargs.get('equipo', None)
        context['id_equipo'] = id_equipo
        return context
    
    def form_valid(self, form):
        id_equipo = self.kwargs.get('equipo', None)
        equipo = Equipo.objects.get(id = id_equipo)
        
        espVer  = form.save(commit=False)
        espVer.id_equipo = equipo
        espVer.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        equipo = self.object.pk
        return reverse('inventario:detalles', kwargs={'pk': equipo})
    
    '''def get_form(self):
         form = super().get_form()
         equipo_id = self.request.session.get('equipo_id')
         print("Se recuperó el dato de sesion equipo_id: ", equipo_id)
         if equipo_id:
              form.fields['id_equipo'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
              print("Se hizo readonly el campo")

         return form

    def get_initial(self):
        initial = super(AgregarEspVerView, self).get_initial()
        id_equipo = self.request.session.get('equipo_id')

        if id_equipo is not None:
            initial['id_equipo'] = id_equipo
            print("id_equipo en initial:", initial['id_equipo'])
        else:
            # Obtén una lista de IDs de equipos que estan registrados en para control metrologico que no tienen un registro en EspecificacionVerificacion
            eq_sin_esp_ids = list(ControlMetro.objects.exclude(
                id_equipo_id__in=EspecificacionVerificacion.objects.values('id_equipo')
            ).values_list('id_equipo', flat=True))

            initial['id_equipo'] = eq_sin_esp_ids

            print("id_equipo en initial:", initial['id_equipo'])

        return initial'''
    
@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class RegistrarVerificacionView(generic.CreateView):
    model = Verificacion
    form_class = VerificacionForm
    template_name = 'verificacion/registroVerificacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        equipo = Equipo.objects.get(id=pk)
        unidad_error = DetalleControlMetro.objects.filter(id_controlMetro=pk, id_criterio="Error").first().id_unidad_criterio
        imagen = equipo.imagen
        if imagen:
            context['img_eq'] = imagen.url
        else:
            context['img_eq'] = "/media/imgs/img/ico_noImage1.png"
        context['id_eq'] = pk
        context['unidad_error'] = unidad_error.id
        return context

    def form_valid(self, form):
        # Asigna el valor de 'pk' de la URL al campo 'id_verificacion' directamente en la vista
        form.instance.id_verificacion_id = self.kwargs['pk']
        especificacion = EspecificacionVerificacion.objects.get(id_equipo=self.kwargs['pk'])
        especificacion.ultima = form.cleaned_data['fecha']
        especificacion.proxima = form.cleaned_data['fecha'] + timedelta(days=30*especificacion.periodo)
        especificacion.save()
        return super(RegistrarVerificacionView, self).form_valid(form)

    def get_success_url(self):
        return reverse('verificacion:verificacion')
    
class HistorialVerificacionView(LoginRequiredMixin, generic.ListView):
    template_name = "verificacion/historialVerificacion.html"
    context_object_name = "registros"

    def get_queryset(self):
        return Verificacion.objects.all()