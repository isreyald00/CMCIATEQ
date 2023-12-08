from argparse import _AttributeHolder
from typing import Any
from django.forms import ValidationError
from django.forms.models import BaseModelForm
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse

from inventario.models import Equipo
from inventario.views import is_in_allowed_groups
from .models import EspecificacionMantenimiento, DetalleMantenimientoExterno, DetalleMantenimientoInterno
from .forms import RegistrarEspManForm, ModificarEspForm, RegistrarMantExtForm,RegistrarMantIntForm

from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from django.conf import settings
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import qrcode
from io import BytesIO
 
class MantenimientoView(LoginRequiredMixin, generic.ListView):
    template_name = "mantenimiento/mantenimiento.html"
    context_object_name = "all_items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipos = context['all_items']
        indicadores = {}

        for equipo in equipos:
            # Almacenar los indicadores en el diccionario
            for equipo in equipos:
                indicadores[equipo.id_equipo] = {
                    'dirEsp': equipo.id_equipo.id_direccion_esp,
                    'sede': equipo.id_equipo.id_sede,
                    'clasificacion': equipo.id_equipo.id_clasificacion,
                    'emailResp': equipo.id_equipo.id_responsable.email,
                    'nombreResp': equipo.id_equipo.id_responsable,
                }
        context['indicadores'] = indicadores
        context['equipos_totales'] = len(equipos)
        return context

    def get_queryset(self):
        return EspecificacionMantenimiento.objects.all()
    
class DetallesEspView(LoginRequiredMixin, generic.DetailView):
    model = EspecificacionMantenimiento
    template_name = "mantenimiento/detallesEspMantenimiento.html"
    context_object_name = 'equipo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = str(self.object.id_equipo)
        equipo = Equipo.objects.get(id=pk)
        img_eq = equipo.imagen
        if img_eq :
            context['img_eq'] = img_eq.url
        else:
            context['img_eq'] = "/media/imgs/img/ico_noImage1.png"
        
        return context


    

class DetallesMantIntView(LoginRequiredMixin, generic.DetailView):
    model = DetalleMantenimientoInterno
    template_name = "mantenimiento/detallesMantenimiento.html"
    context_object_name = 'equipo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = "Interno"
        return context

class DetallesMantExtView(LoginRequiredMixin, generic.DetailView):
    model = DetalleMantenimientoExterno
    template_name = "mantenimiento/detallesMantenimiento.html"
    context_object_name = 'equipo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = "Externo"
        return context

@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class AgregarEspManView(generic.CreateView):
    model = EspecificacionMantenimiento
    form_class = RegistrarEspManForm
    template_name = 'mantenimiento/especificacionMantenimiento.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_equipo = self.kwargs.get('equipo', None)
        context['id_equipo'] = id_equipo
        return context
    
    def form_valid(self, form):
        
        try:
            id_equipo = self.kwargs.get('equipo', None)
            equipo = Equipo.objects.get(id = id_equipo)
            
            esp  = form.save(commit=False)
            esp.id_equipo = equipo

            esp.save()
        except Exception as e:
            messages.error(self.request, f"Error al guardar la especificacion para mantenimiento del equipo {esp.id_equipo}: {e}")
            return super().form_invalid(form)

        return super().form_valid(form)
    
    def get_success_url(self):
        equipo  = self.kwargs.get('equipo', None)
        cal = self.kwargs.get('cal', None)
        ver = self.kwargs.get('ver', None)

        if cal == "1" or ver == "1":
            return reverse ('metrologia:registrarEsp', kwargs={'equipo':equipo, 'cal': cal, 'ver': ver})
        else: 
            return reverse('inventario:detalles', kwargs={'pk': equipo})

    '''def get_form(self):
         form = super().get_form()
         equipo_id = self.request.session.get('equipo_id')
         if equipo_id:
              form.fields['id_equipo'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

         return form

    def get_initial(self):
        initial = super(AgregarEspManView, self).get_initial()
        id_equipo = self.request.session.get('equipo_id')

        if id_equipo is not None:
            initial['id_equipo'] = id_equipo
        else:
            # Obtén una lista de IDs de equipos que no tienen un registro en EspecificacionMantenimiento
            eq_sin_espMant_ids = list(Equipo.objects.exclude(
                id__in=EspecificacionMantenimiento.objects.values('id_equipo')
            ).values_list('id', flat=True))

            initial['id_equipo'] = eq_sin_espMant_ids

            print("id_equipo en initial:", initial['id_equipo'])

        return initial'''
            
@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class ModificarEspView(generic.UpdateView):
    model = EspecificacionMantenimiento
    form_class = ModificarEspForm
    template_name = 'mantenimiento/modificarEspMant.html' 
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_equipo = self.kwargs.get('pk', None)
        context['id_equipo'] = id_equipo
        return context
    
    def form_valid(self, form):
        try:
            with transaction.atomic():
                especificacion = form.save(commit=False)

                if especificacion.periodo <= 0 :
                    raise ValueError("El campo 'Periodo' debe llenarse con un valor mayor a 0")
                
                especificacion.proxima = especificacion.ultima + timedelta(days=30 * especificacion.periodo)
                
                especificacion.save()

                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, e)
            return redirect(self.request.META.get('HTTP_REFERER'))
    
    def get_success_url(self):
        id_equipo = self.kwargs.get('pk', None)
        messages.success(self.request, f"La modificación de la especificación de mantenimiento del equipo {id_equipo} fue realizada exitosamente")
        return reverse('mantenimiento:mantenimiento')

@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class RegistrarMantIntView(generic.CreateView):
    model = DetalleMantenimientoInterno
    form_class = RegistrarMantIntForm
    template_name = 'mantenimiento/registrarMantenimiento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipo = self.kwargs['equipo']
        comentario_equipo = EspecificacionMantenimiento.objects.get(pk = equipo)
        imagen = Equipo.objects.get(pk = self.kwargs['equipo']).imagen
        if imagen :
            imagen_equipo = imagen.url
        else:
            imagen_equipo = "/media/imgs/img/ico_noImage1.png"
        id_usuario = self.request.user.nombre
        context['com_eq']=comentario_equipo
        context['img_eq']=imagen_equipo
        context['id_user']=id_usuario
        context['id_eq']=equipo
        return context

    def get_initial(self):
        initial = super(RegistrarMantIntView, self).get_initial()
        id_usuario = self.request.user.email
        equipo = self.kwargs['equipo']
        initial['id_responsable_cap'] = id_usuario
        initial['id_especificacion_mant'] = equipo
        return initial
   
    def get_success_url(self):
        folio = self.object.num_folio
        return reverse('mantenimiento:detallesInt', kwargs={'pk': folio})

@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class RegistrarMantExtView(generic.CreateView):
    model = DetalleMantenimientoExterno
    form_class = RegistrarMantExtForm
    template_name = 'mantenimiento/registrarMantenimiento.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipo = self.kwargs['equipo']
        comentario_equipo = EspecificacionMantenimiento.objects.get(pk = equipo)
        imagen = Equipo.objects.get(pk = self.kwargs['equipo']).imagen
        if imagen :
            imagen_equipo = imagen.url
        else:
            imagen_equipo = "/media/imgs/img/ico_noImage1.png"
        id_usuario = self.request.user.nombre
        context['com_eq']=comentario_equipo
        context['img_eq']=imagen_equipo
        context['id_user']=id_usuario
        context['id_eq']=equipo
        return context

    def get_initial(self):
        initial = super(RegistrarMantExtView, self).get_initial()
        id_usuario = self.request.user.email
        equipo = self.kwargs['equipo']
        initial['id_responsable_cap'] = id_usuario
        initial['id_especificacion_mant'] = equipo
        return initial
    
    def get_success_url(self):
        folio = self.object.num_folio
        return reverse('mantenimiento:detallesExt', kwargs={'pk': folio})
    
@login_required
def HistorialMantView(request):
    context = {}
    indicadores = {}
    mantInt = DetalleMantenimientoInterno.objects.all()
    mantExt = DetalleMantenimientoExterno.objects.all()

    combinado = []

    for registro in mantInt:
        combinado.append((registro, 'Interno'))
        print(f"Registro fecha: {registro.fecha}")
    for registro in mantExt:
        combinado.append((registro, 'Externo'))
        print(f"Registro fecha: {registro.fecha}")

    print(f"Combinado {combinado}")

    for equipo in combinado:
            print(f"Equipo {equipo[0].id_especificacion_mant}")
            indicadores[equipo[0].id_especificacion_mant] = {
                'dirEsp': equipo[0].id_especificacion_mant.id_equipo.id_direccion_esp,
                'sede': equipo[0].id_especificacion_mant.id_equipo.id_sede,
                'clasificacion': equipo[0].id_especificacion_mant.id_equipo.id_clasificacion,
                'emailResp': equipo[0].id_especificacion_mant.id_equipo.id_responsable.email,
                'nombreResp': equipo[0].id_especificacion_mant.id_equipo.id_responsable,
            }
    
    context['equipos_totales'] = len(combinado)
    context['combinado'] = combinado
    context['indicadores'] = indicadores


    return render( request, 'mantenimiento/historialMantenimiento.html', context)



#GENERACION DE PDF
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
estilo_normal3 = ParagraphStyle(
    'estilo_personalizado3',
    parent=estilos['Normal'],
    fontSize=12,
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
 
def generar_pdf(request, tipo, pk, id):
 
 
    if tipo == 'Interno':
        detalle_mantenimiento = get_object_or_404(DetalleMantenimientoInterno, num_folio=pk)
        txt_res_pro = "Responsable"
        responsable_proveedor = detalle_mantenimiento.id_responsable
 
    elif tipo == 'Externo':
        detalle_mantenimiento = get_object_or_404(DetalleMantenimientoExterno, num_folio=pk)
        txt_res_pro = "Proveedor"
        responsable_proveedor = detalle_mantenimiento.proveedor
 
 
    esp_mantenimiento = get_object_or_404(EspecificacionMantenimiento, id_equipo=id)
    datos_equipo = get_object_or_404(Equipo, id=id)
   
 
    # Obtener la fecha actual en el formato deseado (DD / MM / YYYY)
    fecha_actual = datetime.now().strftime("%d / %m / %Y")
 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename= "Reporte de mantenimiento_{tipo}_{pk}_{id}.pdf"'
 
    # Crear el objeto PDF usando ReportLab
    p = SimpleDocTemplate(response, pagesize=letter)
 
 
 
    # Crea la URL para el código QR (ajusta la URL según tus necesidades)
    qr_url = f"http://127.0.0.1:8000/mantenimiento/detalles{tipo}/{pk}/"
 
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
    espaciador_doble = Spacer(1, 24)
    espaciador_triple = Spacer(1, 32)
    espaciador_pequeño = Spacer(1, 4)
 
    # Estilos de texto
    estilo_normal.alignment = 2
 
    color_rgb = tuple(int(x, 16) / 255.0 for x in ('7B', '2D', '26'))
 
    # Datos para la tabla
    datos_tabla_fecha = [
        ['Fecha de mantenimiento', 'Periodo entre mantenimiento', 'Fecha de próxima mantenimiento'],
        [f'{esp_mantenimiento.ultima}', f'{esp_mantenimiento.periodo} mes(es)', f'{esp_mantenimiento.proxima}'],
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
 
 
 
 
    # Ruta a tu imagen
    ruta_imagen1 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/logo_ciateq.png'
 
    # Crear el objeto de la imagen
    imagen1 = Image(ruta_imagen1, width=90, height=77)
    imagen1.hAlign = 'LEFT'
    imagen1.vAlign = 'TOP'
 
 
    # Obtén la URL de la imagen desde el campo ImageFieldFile
    url_imagen = datos_equipo.codigo_qr.url
 
    # Ruta a tu imagen
    ruta_imagen2 = 'http://127.0.0.1:8000' + url_imagen
 
    # Crear el objeto de la imagen
    imagen2 = Image(ruta_imagen2, width=125, height=125)
    imagen2.hAlign = 'LEFT'
    imagen2.vAlign = 'TOP'
 
 
 
    # Ruta a tu imagen
    ruta_imagen_subtitle1 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/ico_calendar1.png'
 
    # Crear el objeto de la imagen
    imagen_subtitle1 = Image(ruta_imagen_subtitle1, width=18, height=18)
    imagen_subtitle1.vAlign = 'BOTTOM'
 
 
    # Ruta a tu imagen
    ruta_imagen_subtitle2 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/ico_Datosgenerales.png'
 
    # Crear el objeto de la imagen
    imagen_subtitle2 = Image(ruta_imagen_subtitle2, width=18, height=18)
    imagen_subtitle2.vAlign = 'BOTTOM'
 
 
    # Crear el objeto de descripción
    descripcion = Paragraph(f"{detalle_mantenimiento.comentario}", style=estilo_normal2)
 
    # Crear el objeto de fecha de captura
    fecha_captura = Paragraph(f"Fecha de captura: {detalle_mantenimiento.fecha}", estilo_subTitulo1)
 
 
 
 
    # Organizar elementos en dos columnas
    columna_izquierda = [
        ['Folio:', detalle_mantenimiento.num_folio],
        ['Tipo de mantenimiento:', f"{tipo} - {detalle_mantenimiento.tipo_mant}"],
        [txt_res_pro, responsable_proveedor],
        [espaciador, espaciador],
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
        ['Reporte de mantenimiento'],
        [f'Equipo: {esp_mantenimiento.id_equipo}'],
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
        [imagen_subtitle1, 'Fechas de mantenimiento'],
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
        [imagen_subtitle2, 'Comentario'],
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
        [f'Responsable de captura: {detalle_mantenimiento.id_responsable_cap}', f'Fecha de impresión: {fecha_actual}'],
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
                tabla_subtitle1, Spacer(1, 15), tabla_fecha,
                espaciador_triple, tabla_subtitle2, Spacer(1, 10), descripcion,
                ]
 
 
    # Agregar la tabla de criterios a los elementos
    elementos.append(espaciador_triple)
    elementos.append(Spacer(1,80))
    elementos.append(tabla_captura)
 
    p.build(elementos)
 
    # Devuelve la respuesta generada por la función
    return response