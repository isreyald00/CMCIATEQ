from celery import shared_task
from django.utils import timezone
from .models import EspecificacionCalibracion

@shared_task
def cambiar_estatus():
    print("Si entro al cambiar estatus")
    especificaciones = EspecificacionCalibracion.objects.filter(proxima__lte=timezone.now())
    for equipo in especificaciones:
        equipo.estatus = "Fuera de periodo"
        equipo.save()