from io import BytesIO
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect, HttpResponseRedirect, get_object_or_404
import pandas as pd
from django.db import transaction

from django.forms import modelformset_factory
import qrcode


from .forms import ModificarEquipoForm, AgregarEquipoForm, BajaEquipoForm, DetalleDocsForm
from .models import Equipo, DireccionEspecialidad, Sede, Magnitud, Clasificacion, Baja, DetalleDocs
from usuarios.views import is_in_allowed_groups, is_admin_user
from metrologia.models import EspecificacionMetrologia, CriteriosMetrologicos, Unidad, Criterio
from calibracion.models import EspecificacionCalibracion
from verificacion.models import EspecificacionVerificacion
from mantenimiento.models import EspecificacionMantenimiento
from usuarios.models import CustomUser






from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from django.conf import settings
 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class InventarioGralView(LoginRequiredMixin, generic.ListView):
    template_name = "inventario/inventarioGral.html"
    context_object_name = "all_items"

    def get_queryset(self):
        return Equipo.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipos = context['all_items']
        indicadores = {}

        for equipo in equipos:
            necCtrCal = False
            necCal = False
            necVer = False
            necCtrVer = False
            necMant = False
            reqIncert = False

            if self.regCtrlMetro(equipo):
                #Si tiene registro en CtrlMetro
                if not self.regCal(equipo):
                    #No tiene registro en calibración
                    necCal = True
                    if self.necIncertidumbre(equipo):
                        reqIncert = True

                if not self.regVer(equipo):
                    #No tiene registro en verificacion
                    necVer = True
            else:
                #No tiene registro en control metro
                necCtrCal = True
                necCtrVer = True

            if not self.regMant(equipo):
                necMant = True

            # Almacenar los indicadores en el diccionario
            indicadores[equipo.id] = {
                'necCtrCal': necCtrCal,
                'necCal': necCal,
                'necCtrVer': necCtrVer,
                'necVer': necVer,
                'necMant': necMant,
                'reqIncert': reqIncert,
                'emailResp' : equipo.id_responsable.email,
            }
        
        context['indicadores'] = indicadores
        context['equipos_totales'] = len(equipos)
        return context

    def regCal(self, equipo):
        return EspecificacionCalibracion.objects.filter(id_equipo=equipo).exists()

    def regVer(self, equipo):
        return EspecificacionVerificacion.objects.filter(id_equipo=equipo).exists()

    def regMant(self, equipo):
        return EspecificacionMantenimiento.objects.filter(id_equipo=equipo).exists()

    def regCtrlMetro(self, equipo):
        return EspecificacionMetrologia.objects.filter(id_equipo=equipo).exists()
    
    def necIncertidumbre (self, equipo):
        print("Está entrando a la funcion necIncertidubmre")
        ctrlMetro = get_object_or_404(EspecificacionMetrologia, id_equipo = equipo)
        print(CriteriosMetrologicos.objects.filter(id_controlMetro = ctrlMetro, id_criterio = "Incertidumbre"))
        return not CriteriosMetrologicos.objects.filter(id_controlMetro = ctrlMetro, id_criterio = "Incertidumbre").exists()
    
    @method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
    def post(self, request, *args, **kwargs):
        if 'archivo_excel' in request.FILES:
            archivo = request.FILES['archivo_excel']

            try:
                with transaction.atomic():
                    with pd.ExcelFile(archivo) as xls:
                        if ('Inventario General' in xls.sheet_names) and ('Criterios Metrológicos' in xls.sheet_names):
                            df_general = pd.read_excel(archivo, sheet_name='Inventario General', header=[0, 1])
                            datos_generales = df_general['Datos generales']
                            ctrl_metro = df_general['Control metrológico']
                            ctrl_mant = df_general['Control de mantenimiento']
                            for (index, rowDG), (_, rowCM), (_, rowCT) in zip(
                                datos_generales.iterrows(), ctrl_metro.iterrows(), ctrl_mant.iterrows()):
                                try:
                                    if pd.isna(rowDG['Equipo']):
                                        raise ValueError(f"No se pudo guardar el registro de la fila <strong>{str(index)}</strong> debido a que no cuenta con su ID")
                                    
                                    with transaction.atomic():
                                        eq = Equipo.objects.create(
                                            id=rowDG['Equipo'] if pd.notna(rowDG['Equipo']) else None,
                                            activo_fijo=rowDG['Activo fijo'] if pd.notna(rowDG['Activo fijo']) else None,
                                            id_direccion_esp=get_object_or_404(DireccionEspecialidad, id=rowDG['Dirección de especialidad'])if pd.notna(rowDG['Dirección de especialidad']) else None,
                                            id_sede=get_object_or_404(Sede, id=rowDG['Sede']) if pd.notna(rowDG['Sede']) else None,
                                            id_responsable=get_object_or_404(CustomUser, email=rowDG['Email responsable']) if pd.notna(rowDG['Email responsable']) else None,
                                            nombre_eq=rowDG['Nombre del equipo (descripción)'].upper() if pd.notna(rowDG['Nombre del equipo (descripción)']) else None,
                                            marca=rowDG['Marca'] if pd.notna(rowDG['Marca']) else None,
                                            modelo=rowDG['Modelo'] if pd.notna(rowDG['Modelo']) else None,
                                            n_serie=rowDG['No. de serie'] if pd.notna(rowDG['No. de serie']) else None,
                                            id_magnitud=get_object_or_404(Magnitud, id=rowDG['ID Magnitud']) if pd.notna(rowDG['ID Magnitud']) else None,
                                            id_clasificacion=get_object_or_404(Clasificacion, id=rowDG['ID Clasificación']) if pd.notna(rowDG['ID Clasificación']) else None,
                                            id_responsable_alta = request.user,
                                            accesorios=rowDG['Accesorios'] if pd.notna(rowDG['Accesorios']) else None,
                                            estatus=rowDG['Estatus'] if pd.notna(rowDG['Estatus']) else None,
                                            # ... otros campos
                                        )
                                        eq.save()

                                        if not rowCM.isna().all(): #Verifica si en la sección de "Control Metrológico" hay datos.
                                            df_criterios = pd.read_excel(archivo, sheet_name='Criterios Metrológicos')
                                            if (df_criterios['Equipo'] == eq.id).any():
                                                cm = EspecificacionMetrologia.objects.create(
                                                    id_equipo = eq,
                                                    res_unidades = rowCM['Resolución de unidades'] if pd.notna(rowCM['Resolución de unidades']) else None,
                                                    unidades = get_object_or_404(Unidad, id = rowCM['ID de Unidad']) if pd.notna(rowCM['ID de Unidad']) else None,
                                                    intervalo_medicion_unidades = rowCM['Intervalo de medición de unidades'] if pd.notna(rowCM['Intervalo de medición de unidades']) else None
                                                )
                                                cm.save()

                                                crits = df_criterios[(df_criterios['Equipo'] == eq.id)]
                                                for i, crit in crits.iterrows():
                                                    CriteriosMetrologicos.objects.create(
                                                        id_controlMetro = cm,
                                                        rango = crit['Rango'] if pd.notna(crit['Rango']) else None,
                                                        id_criterio = get_object_or_404(Criterio, id = crit['Criterio']) if pd.notna(crit['Criterio']) else None,
                                                        valor_esperado = crit['Valor esperado'] if pd.notna(crit['Valor esperado']) else None,
                                                        id_unidad_criterio = get_object_or_404(Unidad, id = crit['Unidad']) if pd.notna(crit['Unidad']) else None
                                                    )

                                                col_cal = ['Periodo entre calibraciones (meses)',	'Ultima calibración',	'Estatus de calibración']#Definición de las columnas de especificación de calibración.
                                                col_ver = ['Periodo entre verificaciones (meses)',	'Ultima verificación',	'Estatus de verificación']#Definición de las columnas de especificación de verificacion.

                                                if not rowCM[col_cal].isna().all(): #Verificar si el equipo tiene registro para control de calibración
                                                    crit_error = df_criterios[(df_criterios['Equipo'] == eq.id) & (df_criterios['Criterio']== 'Error')]#Verificar que el equipo tenga guardado el criterio de error
                                                    crit_incer = df_criterios[(df_criterios['Equipo'] == eq.id) & (df_criterios['Criterio']== 'Incertidumbre')]#Verificar que el equipo tenga guardado el criterio de incertidumbre
                                                    if (not crit_error.empty) and (not crit_incer.empty):
                                                        EspecificacionCalibracion.objects.create(
                                                            id_equipo = eq,
                                                            periodo = rowCM['Periodo entre calibraciones (meses)'] if pd.notna(rowCM['Periodo entre calibraciones (meses)']) else None,
                                                            ultima = rowCM['Ultima calibración'] if pd.notna(rowCM['Ultima calibración']) else None,
                                                            estatus = rowCM['Estatus de calibración'] if pd.notna(rowCM['Estatus de calibración']) else None
                                                        )
                                                    else:
                                                        raise ValueError(f"El equipo '{eq.id}' SI está registrado para calibración pero NO tiene los criterios de calibración y/o verificacion registrados. Favor de <strong>agregar</strong> los criterios correspondientes o <strong>borrar</strong> los datos de especificación para calibraciones (sección verde).")
                                                        
                                                if not rowCM[col_ver].isna().all():#Verificar si el equipo tiene registro para control de verificación
                                                    crit_error = df_criterios[(df_criterios['Equipo'] == eq.id) & (df_criterios['Criterio']== 'Error')]#Verificar que el equipo tenga guardado el criterio de error
                                                    if not crit_error.empty:
                                                        EspecificacionVerificacion.objects.create(
                                                            id_equipo = eq,
                                                            periodo = rowCM['Periodo entre verificaciones (meses)'] if pd.notna(rowCM['Periodo entre verificaciones (meses)']) else None,
                                                            ultima = rowCM['Ultima verificación'] if pd.notna(rowCM['Ultima verificación']) else None,
                                                            estatus = rowCM['Estatus de verificación'] if pd.notna(rowCM['Estatus de verificación']) else None
                                                        )
                                                    else: 
                                                        raise ValueError(f"El equipo '{eq.id}' SI está registrado para verificación pero NO tiene el criterio de Error registrado. Favor de <strong>agregar</strong> el criterio correspondiente o <strong>borrar</strong> los datos de especificación para verificaciones (sección naranja).")
                                            else:
                                                raise ValueError(f"El equipo '{eq.id}' tiene datos para especificación metrológica pero no tiene criterios registrados.<br>Favor de <strong>agregar</strong> los criterios correspondientes o <strong>borrar</strong> los datos de 'Control Metrológico'.")
                                            
                                            #raise ValueError(f"En la fila {index} hay datos en al menos una columna de Control Metrológico.")
                                        
                                        if not rowCT.isna().all(): #Verifica si en la sección de "Control de mantenimiento" hay datos.
                                            EspecificacionMantenimiento.objects.create(
                                                id_equipo = eq,
                                                periodo = rowCT['Periodo entre mantenimientos'] if pd.notna(rowCT['Periodo entre mantenimientos']) else None,
                                                tipo_periodo = rowCT['horas/dias/meses'] if pd.notna(rowCT['horas/dias/meses']) else None,
                                                tiempo_uso = rowCT['Tiempo de uso (solo en horas)'] if pd.notna(rowCT['Tiempo de uso (solo en horas)']) else None,
                                                ultima = rowCT['Último mantenimiento'] if pd.notna(rowCT['Último mantenimiento']) else None,
                                                estado = rowCT['Estatus de mantenimiento'] if pd.notna(rowCT['Estatus de mantenimiento']) else None,
                                                comentario = rowCT['Comentario'] if pd.notna(rowCT['Comentario']) else None,
                                            )

                                except Exception as e:
                                    messages.error(request, f"<strong>Registro no guardado '{str(rowDG['Equipo'])}':</strong> {str(e)}")
                        else:
                            raise ValueError(f"Archivo incompleto, verifique que se encuentren las hojas <strong>'Inventario General'</strong> y <strong>'Criterios Metrológicos'</strong>")
            except Exception as e:
                # Manejo de errores: Puedes agregar un mensaje de error o redirigir a una página de error
                messages.error(request, f"Error al procesar el archivo: {str(e)}")

        return HttpResponseRedirect(self.request.path_info)  # Redirige nuevamente a la misma página después de procesar el formulario

class DetallesView(LoginRequiredMixin, generic.DetailView):
    model = Equipo
    template_name = "inventario/detallesEquipo.html"
    context_object_name = 'equipo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipo = context['equipo']

        # Esto devolverá la primera instancia que encuentre o None si no se encuentra ninguna.
        context['EspecificacionMetrologia'] = EspecificacionMetrologia.objects.filter(id_equipo=equipo).first()
        context['EspecificacionCalibracion'] = EspecificacionCalibracion.objects.filter(id_equipo=equipo).first()
        context['EspecificacionVerificacion'] = EspecificacionVerificacion.objects.filter(id_equipo=equipo).first()
        context['EspecificacionMantenimiento'] = EspecificacionMantenimiento.objects.filter(id_equipo=equipo).first()
        context['CriteriosMetrologicos'] = CriteriosMetrologicos.objects.filter(id_controlMetro = context['EspecificacionMetrologia'])
        
        return context

@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class ModificarEquipoView(generic.UpdateView):
    model = Equipo
    form_class = ModificarEquipoForm
    template_name = 'inventario/modificarEquipo.html'

    def get_success_url(self):
        return reverse('inventario:inventarioGral')

@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class AgregarEquipoView(generic.CreateView):
    model = Equipo
    form_class = AgregarEquipoForm
    template_name = 'inventario/agregarEquipo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DetDocsFormset = modelformset_factory(DetalleDocs, form=DetalleDocsForm, fields=('url',), extra=0, min_num=1)
        formset = DetDocsFormset(self.request.POST or None, self.request.FILES or None, queryset=DetalleDocs.objects.none(), prefix='detalle_docs')
        
        context['formset'] = formset
        return context

    def form_valid(self, form):
        equipo = form.save(commit=False)
        equipo.id_responsable_alta = self.request.user
        equipo.save() 

        # Recuperar el formset del contexto
        formset = self.get_context_data().get('formset')
        print(self.request.POST)
        if formset and formset.is_valid():
            for detalle_form in formset:
                detalle = detalle_form.save(commit=False)
                if detalle.url:
                    detalle.id_equipo = equipo
                    print(f"Url del doc: {detalle.url}")
                    detalle.save()
        else:
            print("Lo detecto como no valido")
            print(formset.errors)
            return self.form_invalid(form)


        mant = form.cleaned_data['necesita_mant'] == "Si"
        cal =  form.cleaned_data['necesita_cal'] == "Si"
        ver =  form.cleaned_data['necesita_ver'] == "Si"

        if cal or ver or mant:
            if cal and ver and mant:
                return redirect('mantenimiento:registrarEsp', equipo=equipo.id, cal="1", ver="1")
            elif mant:
                if cal:
                    return redirect('mantenimiento:registrarEsp', equipo=equipo.id, cal="1", ver="0")
                elif ver:
                    return redirect('mantenimiento:registrarEsp', equipo=equipo.id, cal="0", ver="1")
                else:
                    return redirect('mantenimiento:registrarEsp', equipo=equipo.id, cal="0", ver="0")
            elif cal:
                if ver:
                    return redirect('metrologia:registrarEsp', equipo=equipo.id, cal="1", ver="1")
                else:
                    return redirect('metrologia:registrarEsp', equipo=equipo.id, cal="1", ver="0")
            elif ver:
                return redirect('metrologia:registrarEsp', equipo=equipo.id, cal="0", ver="1")
        else:
            return redirect('inventario:detalles', pk = equipo.id)

@method_decorator(user_passes_test(is_admin_user), name='dispatch')
class BajaEquipoView(generic.CreateView):
    model = Baja
    form_class = BajaEquipoForm
    template_name = 'inventario/bajaEquipo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_equipo = self.kwargs.get('equipo', None)
        equipo = Equipo.objects.filter(id = id_equipo).first()
        context['equipo'] = id_equipo
        context['responsable'] = equipo.id_responsable
        return context

    def form_valid(self, form):
        id_equipo = self.kwargs.get('equipo', None)
        equipo = Equipo.objects.filter(id=id_equipo).first()
        baja = form.save(commit=False)
        baja.id_equipo = equipo
        baja.save()
        equipo.estatus = "Baja"
        equipo.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        id_equipo = self.kwargs.get('equipo', None)
        return redirect('inventario:detalles', pk = id_equipo)

class DocsView(LoginRequiredMixin, generic.ListView):
    template_name = "inventario/docs.html"
    context_object_name = "all_items"

    def get_queryset(self):
        equipo = self.kwargs.get('equipo')
        return DetalleDocs.objects.filter(id_equipo = equipo)



#GENERAR PDF        
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
    'estilo_personalizadoT',
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
 
def generar_pdf(request, pk):
    equipo = get_object_or_404(Equipo, id=pk)
    
    # Verificar si hay registros para calibracion
    try:
        calibracion = EspecificacionCalibracion.objects.get(id_equipo=pk)
    except EspecificacionCalibracion.DoesNotExist:
        calibracion = None
    
    # Verificar si hay registros para verificacion
    try:
        verificacion = EspecificacionVerificacion.objects.get(id_equipo=pk)
    except EspecificacionVerificacion.DoesNotExist:
        verificacion = None
    
    # Verificar si hay registros para mantenimiento
    try:
        mantenimiento = EspecificacionMantenimiento.objects.get(id_equipo=pk)
    except EspecificacionMantenimiento.DoesNotExist:
        mantenimiento = None
    
    # Verificar si hay registros para Control_Metro
    try:
        Control_Metro = EspecificacionMetrologia.objects.get(id_equipo=pk)
    except EspecificacionMetrologia.DoesNotExist:
        Control_Metro = None

    # Verificar si hay registros para Criterios_data
    try:
        Criterios_data = CriteriosMetrologicos.objects.filter(id_controlMetro=pk)
    except CriteriosMetrologicos.DoesNotExist:
        Criterios_data = None

    

    # Obtener la fecha actual en el formato deseado (DD / MM / YYYY)
    fecha_actual = datetime.now().strftime("%d / %m / %Y")
 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename= "Detalles de equipo_{pk}.pdf"'
 
    # Crear el objeto PDF usando ReportLab
    p = SimpleDocTemplate(response, pagesize=letter)
 


    # Crea la URL para el código QR (ajusta la URL según tus necesidades)
    qr_url = f"http://http://127.0.0.1:8000/inventarioGral/detallesEquipo/{pk}/"
 
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

 
    # Organizar elementos en dos columnas
    columna_izquierda_datos = [
        ['Nombre de equipo:', equipo.nombre_eq],
        ['Activo fijo:', equipo.activo_fijo],
        ['Dir. de especialidad:', equipo.id_direccion_esp.nombre],
        ['Magnitud:', equipo.id_magnitud.nombre],
        ['Sede:', equipo.id_sede.nombre],
        ['Responsable:', equipo.id_responsable],
        ['Marca:', equipo.marca],
    ]
 
    columna_derecha_datos = [
        ['Modelo:', equipo.modelo],
        ['Número de Serie:', equipo.n_serie],
        ['Fecha de alta:', equipo.fecha_alta],
        ['Accesorios:', equipo.accesorios],
        ['Clasificación:', equipo.id_clasificacion.nombre],
        ['Responsable de la alta:', equipo.id_responsable_alta],
        ['Estatus del equipo:', equipo.estatus],
    ]
 
    # Establecer estilos para la tabla izquierda
    estilo_tabla_izquierda_datos = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Alinea la primera columna a la izquierda
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Alinea la segunda columna al centro
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Ajusta el espacio entre las filas
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agrega bordes negros a la tabla
    ])
 
    # Establecer estilos para la tabla
    estilo_tabla_derecha_datos = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Alinea la primera columna a la izquierda
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Alinea la segunda columna al centro
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Ajusta el espacio entre las filas
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agrega bordes negros a la tabla
    ])
 
    # Crear tablas para cada columna
    tabla_izquierda_datos = Table(columna_izquierda_datos, colWidths='*')
    tabla_derecha_datos = Table(columna_derecha_datos, colWidths='*')
 
    # Aplicar estilos a las tablas
    tabla_izquierda_datos.setStyle(estilo_tabla_izquierda_datos)
    tabla_derecha_datos.setStyle(estilo_tabla_derecha_datos)
 
    # Organizar ambas tablas en una tabla principal
    tabla_principal_data_datos = [
        [tabla_izquierda_datos, tabla_derecha_datos],
    ]
 
    tabla_principal_datos = Table(tabla_principal_data_datos, colWidths=[290, 290])  # Ajusta el ancho de las columnas según sea necesario
 

 
 
    # Ruta a tu imagen
    ruta_imagen1 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/logo_ciateq.png'
 
    # Crear el objeto de la imagen
    imagen1 = Image(ruta_imagen1, width=90, height=77)
    imagen1.hAlign = 'LEFT'
    imagen1.vAlign = 'TOP'

 
    # Ruta a tu imagen
    ruta_imagen_subtitle1 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/ico_Datosgenerales.png'
 
    # Crear el objeto de la imagen
    imagen_subtitle1 = Image(ruta_imagen_subtitle1, width=18, height=18)
    imagen_subtitle1.vAlign = 'BOTTOM'
 
 
    # Ruta a tu imagen
    ruta_imagen_subtitle2 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/ico_EspecificacionMetrologica.png'
 
    # Crear el objeto de la imagen
    imagen_subtitle2 = Image(ruta_imagen_subtitle2, width=18, height=18)
    imagen_subtitle2.vAlign = 'BOTTOM'


    # Ruta a tu imagen
    ruta_imagen_subtitle3 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/ico_calendar1.png'
 
    # Crear el objeto de la imagen
    imagen_subtitle3 = Image(ruta_imagen_subtitle3, width=18, height=18)
    imagen_subtitle3.vAlign = 'BOTTOM'
 
 
    # Ruta a tu imagen
    ruta_imagen_subtitle4 = 'http://127.0.0.1:8000' + settings.MEDIA_URL + 'imgs/img/ico_mantenimiento1.png'
 
    # Crear el objeto de la imagen
    imagen_subtitle4 = Image(ruta_imagen_subtitle4, width=18, height=18)
    imagen_subtitle4.vAlign = 'BOTTOM'
 

    # Ruta a tu imagen
    url_imagen = equipo.imagen
    ruta_imagen_equipo = 'http://127.0.0.1:8000' + equipo.imagen.url
 
    # Crear el objeto de la imagen
    imagen_equipo = Image(ruta_imagen_equipo, width=155, height=125)
 

    # Crear el objeto de fecha de captura
    fecha_captura = Paragraph(f"Fecha de captura: {fecha_actual}", estilo_subTitulo1)

    # Crear el objeto de fecha de captura
    fecha_impresion = Paragraph(f"Fecha de impresión: {fecha_actual}", estilo_subTitulo1)
 
 


    # Organizar elementos en dos columnas
    columna_izquierda = [
        [imagen_equipo],
 
    ]
 
    columna_derecha = [
        [image_QR],
    ]
 
    # Establecer estilos para la tabla izquierda
    estilo_tabla_izquierda = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Alinea la primera columna a la izquierda
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Alinea la segunda columna al centro
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Ajusta el espacio entre las filas
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ])
 
    # Establecer estilos para la tabla
    estilo_tabla_derecha = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
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
 
    tabla_principal = Table(tabla_principal_data, colWidths=[180, 180])  # Ajusta el ancho de las columnas según sea necesario
 

 
    # Organizar elementos en dos columnas
    columna_izquierda1 = [
        [imagen1],
    ]
 
    columna_derecha1 = [
        ['Detalles de equipo'],
        [f'Equipo: {pk}'],
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
        [imagen_subtitle1, 'Datos generales'],
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
 







    if Control_Metro:
        def crear_tabla_dinamica_criterios(criterios_data):
            # Crear una lista para almacenar las filas de la tabla
            filas_tabla = []
        
            # Encabezados de la tabla
            encabezados = ["Criterio", "Rango", "Valor Esperado"]
            filas_tabla.append(encabezados)
        
            # Agregar datos de criterios a la tabla
            for criterio in criterios_data:
                fila = [criterio[0], criterio[1], criterio[2]]
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
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agrega bordes negros a la tabla
            ])
        
            # Aplicar estilos a la tabla
            tabla_criterios.setStyle(estilo_tabla_criterios)
        
            return tabla_criterios


        # Datos para la tabla
        datos_tabla_subtitle2 = [
            [imagen_subtitle2, 'Control metrológico'],
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




        # Agregar la tabla de criterios dinámica
        criterios_data = [
        (detalle.id_criterio, detalle.rango, f"{detalle.valor_esperado} {detalle.id_unidad_criterio.id}")
        for detalle in Criterios_data
        ]
 
        # Llamar a la función para crear la tabla de criterios
        tabla_criterios = crear_tabla_dinamica_criterios(criterios_data)




        # Organizar elementos en dos columnas
        columna_izquierda_metro = [
            ['Unidades:', Control_Metro.unidades],
            ['Resolución de unidades:', Control_Metro.res_unidades],
            ['Int. de medición de unidades:', Control_Metro.intervalo_medicion_unidades],
        ]
    
        # Establecer estilos para la tabla izquierda
        estilo_tabla_izquierda_metro = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Alinea la primera columna a la izquierda
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Alinea la segunda columna al centro
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Ajusta el espacio entre las filas
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agrega bordes negros a la tabla
        ])
 
        # Crear tablas para cada columna
        tabla_izquierda_metro = Table(columna_izquierda_metro, colWidths=[180,100])
        
        # Aplicar estilos a las tablas
        tabla_izquierda_metro.setStyle(estilo_tabla_izquierda_metro)
        
         # Organizar ambas tablas en una tabla principal
        tabla_principal_data_metro = [
            [tabla_izquierda_metro, tabla_criterios],
        ]
        
        tabla_principal_metro = Table(tabla_principal_data_metro, colWidths=[330, 250])  # Ajusta el ancho de las columnas según sea necesario







    if calibracion:
        # Datos para la tabla
        datos_tabla_subtitle3 = [
            [imagen_subtitle2, 'Calibración'],
        ]
    
        # Crear la tabla
        tabla_subtitle3 = Table(datos_tabla_subtitle3)
    
        # Establecer estilos para la tabla
        estilo_tabla_subtitle3 = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
        ])
    
        # Aplicar estilos a la tabla
        tabla_subtitle3.setStyle(estilo_tabla_subtitle3)
        tabla_subtitle3.hAlign = 0



        # Datos para la tabla
        datos_tabla_fecha_cal = [
            ['Ultima calibración', 'Periodo entre calibración', 'Próxima calibración', 'Confirmación metrológica'],
            [f'{calibracion.ultima}', f'{calibracion.periodo} meses', f'{calibracion.proxima}', f'{calibracion.estatus}'],
        ]
    
        # Especifica el ancho máximo para cada columna
        ancho_maximo_columnas = [120, 150, 120, 150]

        # Crear la tabla
        tabla_fecha_cal = Table(datos_tabla_fecha_cal, colWidths=ancho_maximo_columnas)
    
        # Establecer estilos para la tabla
        estilo_tabla_fecha_cal = TableStyle([
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
        tabla_fecha_cal.setStyle(estilo_tabla_fecha_cal)






    if verificacion:
        # Datos para la tabla
        datos_tabla_subtitle4 = [
            [imagen_subtitle2, 'Verificación'],
        ]
    
        # Crear la tabla
        tabla_subtitle4 = Table(datos_tabla_subtitle4)
    
        # Establecer estilos para la tabla
        estilo_tabla_subtitle4 = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
        ])
 
        # Aplicar estilos a la tabla
        tabla_subtitle4.setStyle(estilo_tabla_subtitle4)
        tabla_subtitle4.hAlign = 0




        # Datos para la tabla
        datos_tabla_fecha_ver = [
            ['Ultima verificación', 'Periodo entre verificaciones', 'Próxima verificación', 'Confirmación metrológica'],
            [f'{verificacion.ultima}', f'{verificacion.periodo} mes(es)', f'{verificacion.proxima}', f'{verificacion.estatus}'],
        ]
    
        # Especifica el ancho máximo para cada columna
        ancho_maximo_columnas2 = [118, 154, 118, 150]

        # Crear la tabla
        tabla_fecha_ver = Table(datos_tabla_fecha_ver, colWidths=ancho_maximo_columnas2)
    
        # Establecer estilos para la tabla
        estilo_tabla_fecha_ver = TableStyle([
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
        tabla_fecha_ver.setStyle(estilo_tabla_fecha_ver)








    if mantenimiento:
        # Datos para la tabla
        datos_tabla_subtitle5 = [
            [imagen_subtitle4, 'Mantenimiento'],
        ]
    
        # Crear la tabla
        tabla_subtitle5 = Table(datos_tabla_subtitle5)
    
        # Establecer estilos para la tabla
        estilo_tabla_subtitle5 = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
        ])
    
        # Aplicar estilos a la tabla
        tabla_subtitle5.setStyle(estilo_tabla_subtitle5)
        tabla_subtitle5.hAlign = 0


    
        # Datos para la tabla
        datos_tabla_fecha_man = [
            ['Ultimo mantenimiento', 'Periodo entre mantenimiento', 'Próximo mantenimiento', 'Estado'],
            [f'{mantenimiento.ultima}', f'{mantenimiento.periodo} mes(es)', f'{mantenimiento.proxima}', f'{mantenimiento.estado}'],
        ]
    
        # Especifica el ancho máximo para cada columna
        ancho_maximo_columnas3 = [134, 164, 134, 108]

        # Crear la tabla
        tabla_fecha_man = Table(datos_tabla_fecha_man, colWidths=ancho_maximo_columnas3)
    
        # Establecer estilos para la tabla
        estilo_tabla_fecha_man = TableStyle([
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
        tabla_fecha_man.setStyle(estilo_tabla_fecha_man)

 


 
    # Agregar elementos al PDF
    elementos = [
                fecha_impresion, espaciador, tabla_principal1, Spacer(1, 5), tabla_principal, Spacer(1, 15),
                tabla_subtitle1, Spacer(1, 10), tabla_principal_datos,
                ]

    if Control_Metro:
        elementos.extend([Spacer(1, 30), tabla_subtitle2, Spacer(1, 7), tabla_principal_metro,])

    if calibracion:
        elementos.extend([Spacer(1, 25), tabla_subtitle3, Spacer(1, 10), tabla_fecha_cal,])

    if verificacion:
        elementos.extend([Spacer(1, 35), tabla_subtitle4, Spacer(1, 10), tabla_fecha_ver,])

    if mantenimiento:
        elementos.extend([Spacer(1, 35), tabla_subtitle5, Spacer(1, 10), tabla_fecha_man,])

    


 
    p.build(elementos)
 
    # Devuelve la respuesta generada por la función
    return response