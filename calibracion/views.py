from io import BytesIO
from django.contrib import messages
from django.forms.models import BaseModelForm
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ValidationError, formset_factory
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import timedelta

import qrcode

from inventario.views import is_in_allowed_groups
from inventario.models import Equipo
from metrologia.models import CriteriosMetrologicos
from .models import EspecificacionCalibracion, Calibracion, CriteriosCalibracion
from .forms import RegistrarEspCalForm, CalibracionForm, CriteriosCalibracionForm, ModificarEspForm

from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from django.conf import settings
 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
 

class CalibracionView(LoginRequiredMixin, generic.ListView):
    template_name = "calibracion/calibracion.html"
    context_object_name = "all_items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipos = context['all_items']
        indicadores = {}

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
        return EspecificacionCalibracion.objects.all()

@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class AgregarEspCalView(generic.CreateView):
    model = EspecificacionCalibracion
    form_class = RegistrarEspCalForm
    template_name = 'calibracion/especificacionCalibracion.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_equipo = self.kwargs.get('equipo', None)
        context['id_equipo'] = id_equipo
        return context
    
    def form_valid(self, form):
        id_equipo = self.kwargs.get('equipo', None)
        equipo = Equipo.objects.get(id=id_equipo)

        esp = form.save(commit=False)
        esp.id_equipo = equipo
        esp.save()
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Agrega mensajes de error al contexto de la respuesta
        messages.error(self.request, 'Error en el formulario. Por favor, verifica los datos.')
        return super().form_invalid(form)

    def get_success_url(self):
        ver = self.kwargs.get('ver', None)
        equipo = self.object.pk
        if ver == "1":
            return reverse('verificacion:registrarEsp', kwargs={'equipo': equipo})
        else:
            return reverse('inventario:detalles', kwargs={'pk': equipo})
        
@user_passes_test(is_in_allowed_groups)
def RegistrarCalibracionView(request, pk):
    context = {}
    especificacion_id = pk
    imagen = Equipo.objects.get(pk = especificacion_id).imagen
    criterios_metro = CriteriosMetrologicos.objects.filter(id_controlMetro=especificacion_id)
    especificacion = EspecificacionCalibracion.objects.get(id_equipo = especificacion_id)
    criterios = [(criterio.id, criterio.id_criterio, criterio.id_unidad_criterio.id, criterio.valor_esperado, criterio.rango) for criterio in criterios_metro]
    criterios_dict = {
        criterio[0]: {
            'nombre': criterio[1],
            'unidad': criterio[2],
            'valor_esperado': criterio[3],
            'rango': criterio[4]
        }
        for criterio in criterios
    }
    print("Criterios a tomar en cuenta: ", criterios)
    CritCalFormset = formset_factory(CriteriosCalibracionForm, extra=0, min_num=len(criterios))

    if request.method == "POST":
        # Crea el formulario con request.FILES para manejar archivos adjuntos
        form = CalibracionForm(request.POST, request.FILES, initial={'id_especificacion': especificacion_id})
        formset = CritCalFormset(request.POST, prefix='criterios_calibracion')
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    calibracion = form.save(commit=False)
                    calibracion.resp_cap = request.user

                    extension = calibracion.doc.name.split('.')[-1]
                    new_name = f'Certificado_Calibracion_{calibracion.cod_cer_cal}.{extension}'
                    calibracion.doc.name = new_name

                    calibracion.save()

                    i = 0
                    resultados = []
                    resultado =""
                    for crit_form in formset:
                        criterio = crit_form.save(commit=False)
                        criterio.cod_cer_cal = calibracion
                        if str(criterios[i][4]) == "=":
                            if criterio.valor == criterios[i][3]:
                                resultados.append(True)
                            else:
                                resultados.append(False)
                        elif str(criterios[i][4]) == "Max":
                            if criterio.valor <= criterios[i][3]:
                                resultados.append(True)
                            else:
                                resultados.append(False)
                        elif str(criterios[i][4]) == "Min":
                            if criterio.valor >= criterios[i][3]:
                                resultados.append(True)
                            else:
                                resultados.append(False)
                        else:
                            if criterio.valor == criterios[i][3]:
                                resultados.append(True)
                            else:
                                resultados.append(False)
                        i = i+1
                        criterio.save()
                    print(resultados)
                    if all(resultados):
                        resultado = "Conforme"
                    else: 
                        resultado = "No Conforme"

                    calibracion.dictamen = resultado
                    print(f"Doc antes de guardar: {calibracion.doc}")
                    calibracion.save()

                    especificacion.ultima = calibracion.fecha
                    especificacion.proxima = especificacion.ultima + timedelta(days=30 * especificacion.periodo)
                    especificacion.save()

                    messages.success(request, "Calibración registrada exitosamente")
                    return redirect('calibracion:detalles', pk = calibracion.cod_cer_cal)
            except Exception as e:
                messages.error(request, f"Error: {e}")

    else:
        initial_values = [{'id_criterio': criterio[0]} for criterio in criterios]
        # Crea el formulario sin request.FILES en caso de no ser una solicitud POST
        form = CalibracionForm(initial={'id_especificacion': especificacion_id})
        formset = CritCalFormset(prefix='criterios_calibracion', initial=initial_values)

    context['formset'] = formset
    context['form'] = form
    context['id_equipo'] = especificacion_id
    context['criterios_dict'] = criterios_dict
    if imagen:
        context['img_eq'] = imagen.url
    else:
        context['img_eq'] = "/media/imgs/img/ico_noImage1.png"
    return render(request, 'calibracion/registroCalibracion.html', context)

class HistorialCalibracionView(LoginRequiredMixin, generic.ListView):
    template_name = "calibracion/historialCalibracion.html"
    context_object_name = "registros"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = context['registros']
        indicadores = {}

        # Almacenar los indicadores en el diccionario
        for equipo in registros:
            indicadores[equipo.id_especificacion] = {
                'dirEsp': equipo.id_especificacion.id_equipo.id_direccion_esp,
                'sede': equipo.id_especificacion.id_equipo.id_sede,
                'clasificacion': equipo.id_especificacion.id_equipo.id_clasificacion,
                'emailResp': equipo.id_especificacion.id_equipo.id_responsable.email,
                'nombreResp': equipo.id_especificacion.id_equipo.id_responsable,
            }


        context['indicadores'] = indicadores
        context['equipos_totales'] = len(registros)
        return context

    def get_queryset(self):
        return Calibracion.objects.all()
    
@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class ModificarEspView(generic.UpdateView):
    model = EspecificacionCalibracion
    form_class = ModificarEspForm
    template_name = 'calibracion/modificarEspCal.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_equipo = self.kwargs.get('pk', None)
        context['id_equipo'] = id_equipo
        return context
    
    def form_valid(self, form):
        try:
            with transaction.atomic():
                especificacion = form.save(commit=False)
                
                if especificacion.proxima:
                    especificacion.proxima = especificacion.ultima + timedelta(days=30 * especificacion.periodo)
                
                especificacion.save()

                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, e)
            return redirect(self.request.META.get('HTTP_REFERER'))

    def get_success_url(self):
        id_equipo = self.kwargs.get('pk', None)
        messages.success(self.request, f"La modificación del periodo  de calibración del equipo {id_equipo} fue realizada exitosamente")
        return reverse('calibracion:calibracion')
    
class DetallesCalView(LoginRequiredMixin, generic.DetailView):
    model = Calibracion
    template_name = "calibracion/detallesCalibracion.html"
    context_object_name = 'calibracion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calibracion = self.object  # Obtener la instancia de Calibracion
        criterios = CriteriosCalibracion.objects.filter(cod_cer_cal=calibracion).select_related('id_criterio')
        criterios_data = [(criterio.id_criterio, criterio.valor, criterio.id_criterio.valor_esperado, criterio.id_criterio.id_unidad_criterio) for criterio in criterios]
        '''criterios_dict = {
            criterio[0]: {
                'valor_esperado': criterio[2],
                'valor_obtenido': criterio[1],
                'unidad': criterio[3]
            }
            for criterio in criterios_data
        } '''
        equipo = Equipo.objects.get(id=calibracion.id_especificacion)
        img_eq = equipo.imagen.url
        print(type(criterios_data))
        print("Criterios Data: ", criterios_data)
        context['criterios_data'] = criterios_data
        context['img_eq'] = img_eq
        return context




#GENERACIÓN DE PDF
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
 
 
def generar_pdf(request, pk, id):
    especificacion_calibracion = get_object_or_404(EspecificacionCalibracion, id_equipo=pk)
    datos_equipo = get_object_or_404(Equipo, id=pk)
    calibracion = get_object_or_404(Calibracion, cod_cer_cal=id)
    detalle_control_metro = CriteriosCalibracion.objects.filter(cod_cer_cal=calibracion.cod_cer_cal).select_related('id_criterio')
 
    # Obtener la fecha actual en el formato deseado (DD / MM / YYYY)
    fecha_actual = datetime.now().strftime("%d / %m / %Y")
 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename= "Reporte de calibración_{calibracion.cod_cer_cal}_{datos_equipo.fecha_alta}.pdf"'
 
    # Crear el objeto PDF usando ReportLab
    p = SimpleDocTemplate(response, pagesize=letter)
 

 
 
    # Crea la URL para el código QR (ajusta la URL según tus necesidades)
    qr_url = f"http://127.0.0.1:8000/calibracion/detalles/{calibracion.cod_cer_cal}/"
 
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
        ['Fecha de calibración', 'Periodo entre calibraciones', 'Fecha de próxima calibración'],
        [f'{especificacion_calibracion.ultima}', f'{especificacion_calibracion.periodo} meses', f'{especificacion_calibracion.proxima}'],
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
    datos_tabla_dictamen = [
        ['Confirmación metrológica'],
        [f'{calibracion.dictamen}'],
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

    # Crear el objeto de ID de equipo
    id_equipo = Paragraph(f"Equipo: {especificacion_calibracion.id_equipo}", style=estilo_normal1)
    id_equipo.hAlign = 'CENTER'
 
 
 
    # Organizar elementos en dos columnas
    columna_izquierda = [
        ['Código del certificado de calibración:', calibracion.cod_cer_cal],
        ['Proveedor de calibración:', calibracion.proveedor],
        ['Patrón utilizado:', calibracion.id_patron],
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
        ['Reporte de calibración'],
        [f'Equipo: {especificacion_calibracion.id_equipo}'],
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
        [imagen_subtitle1, 'Fechas de calibración'],
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
        [imagen_subtitle2, 'Detalles de calibración'],
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
        [f'Responsable de captura: {calibracion.resp_cap}', f'Fecha de impresión: {fecha_actual}'],
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
                espaciador_triple, tabla_subtitle2, Spacer(1, 10),
                ]
   
    # Agregar la tabla de criterios dinámica
    criterios_data = [
    (detalle.id_criterio.id_criterio, detalle.id_criterio.valor_esperado, detalle.valor, detalle.id_criterio.id_unidad_criterio.nombre)
    for detalle in detalle_control_metro
    ]
 
 
    # Llamar a la función para crear la tabla de criterios
    tabla_criterios = crear_tabla_dinamica_criterios(criterios_data)
 
 
    # Agregar la tabla de criterios a los elementos
    elementos.append(tabla_criterios)
    elementos.append(espaciador_triple)
    elementos.append(tabla_dictamen)
    elementos.append(Spacer(1,40))
    elementos.append(tabla_captura)
 
    p.build(elementos)
 
    # Devuelve la respuesta generada por la función
    return response
 
def crear_tabla_dinamica_criterios(criterios_data):
    # Crear una lista para almacenar las filas de la tabla
    filas_tabla = []
 
    # Encabezados de la tabla
    encabezados = ["Criterio", "Valor Esperado", "Valor Obtenido", "Unidad"]
    filas_tabla.append(encabezados)
 
    # Agregar datos de criterios a la tabla
    for criterio in criterios_data:
        fila = [criterio[0], criterio[1], criterio[2], criterio[3]]
        filas_tabla.append(fila)
 
    # Crear la tabla
    tabla_criterios = Table(filas_tabla)
 
    color_rgb = tuple(int(x, 16) / 255.0 for x in ('7B', '2D', '26'))
 
    # Establecer estilos para la tabla
    estilo_tabla_criterios = TableStyle([
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
    tabla_criterios.setStyle(estilo_tabla_criterios)
 
    return tabla_criterios
