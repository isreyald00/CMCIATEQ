from typing import Any
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

from calibracion.models import EspecificacionCalibracion
from verificacion.models import EspecificacionVerificacion
from mantenimiento.models import EspecificacionMantenimiento

class CalendarioView(LoginRequiredMixin, generic.ListView):
    template_name = "calendario/calendario.html"
    context_object_name = "eventos"

    def get_queryset(self):
        calibraciones = EspecificacionCalibracion.objects.all()
        verificaciones = EspecificacionVerificacion.objects.all()
        mantenimientos = EspecificacionMantenimiento.objects.all()

        eventos = []

        for evento in calibraciones:
            if evento.proxima:
                evento.color = '#C6EFCE'
                evento.tipo = 'Calibración'
                evento.responsable = evento.id_equipo.id_responsable
                evento.emailResp = evento.id_equipo.id_responsable.email
                evento.dirEsp = evento.id_equipo.id_direccion_esp
                evento.sede = evento.id_equipo.id_sede
                evento.clasificacion = evento.id_equipo.id_clasificacion

                eventos.append(evento)

        for evento in verificaciones:
            if evento.proxima:
                evento.color = '#FFCC99'
                evento.tipo = 'Verificación'
                evento.responsable = evento.id_equipo.id_responsable
                evento.emailResp = evento.id_equipo.id_responsable.email
                evento.dirEsp = evento.id_equipo.id_direccion_esp
                evento.sede = evento.id_equipo.id_sede
                evento.clasificacion = evento.id_equipo.id_clasificacion
                eventos.append(evento)

        for evento in mantenimientos:
            if evento.proxima:
                evento.color = '#FFC7CE'
                evento.tipo = 'Mantenimiento'
                evento.responsable = evento.id_equipo.id_responsable
                evento.emailResp = evento.id_equipo.id_responsable.email
                evento.dirEsp = evento.id_equipo.id_direccion_esp
                evento.sede = evento.id_equipo.id_sede
                evento.clasificacion = evento.id_equipo.id_clasificacion
                eventos.append(evento)

        return eventos
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        eventos = context['eventos']
        context['eventos_totales'] = len(eventos)
        return context
    
  