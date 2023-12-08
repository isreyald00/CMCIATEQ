from django.db import models
from django.conf import settings
from django.forms import ValidationError
from inventario.models import Equipo
from metrologia.models import CriteriosMetrologicos
from datetime import timedelta, date

class EspecificacionCalibracion(models.Model):
    id_equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, primary_key=True)
    periodo = models.IntegerField(null=False, blank= False)
    ultima = models.DateField(null=True, blank= True)
    proxima = models.DateField(null=True, blank= True)
    estatus = models.CharField(max_length=20, null=False, blank= False, default="Pendiente")

    def clean(self):
        if self.periodo < 1:
            raise ValidationError({'periodo': 'El valor del Periodo debe ser mayor que 0.'})
        if self.ultima and self.ultima > date.today():
            raise ValidationError({'ultima': 'La fecha de última calibración debe ser anterior a la fecha actual.'})
        if self.proxima and self.proxima < date.today():
            raise ValidationError({'proxima': 'La fecha de próxima calibración debe ser posterior a la fecha actual.'})
        return super().clean()
    


    def __str__(self):
        return str(self.id_equipo)  # Convierte el objeto a una cadena antes de devolverlo

class Calibracion(models.Model):
    cod_cer_cal = models.CharField(max_length=25, primary_key=True)
    id_especificacion = models.ForeignKey(EspecificacionCalibracion, on_delete=models.CASCADE)
    fecha = models.DateField(null=False, blank=False)
    fecha_cap = models.DateField(auto_now_add=True)
    proveedor = models.CharField(max_length=50, null=False, blank=False)
    id_patron = models.CharField(max_length=100)
    doc = models.FileField(upload_to='docs/calibracion')
    dictamen = models.CharField(max_length=11)
    resp_cap = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True)

    def clean(self):
        if self.fecha > date.today():
            raise ValidationError({'fecha': 'La fecha de calibración no debe ser posterior a la fecha actual.'})
        return super().clean()

    def __str__(self):
        return str(self.cod_cer_cal)  # Convierte el objeto a una cadena antes de devolverlo

class CriteriosCalibracion(models.Model):
    cod_cer_cal = models.ForeignKey(Calibracion, on_delete=models.DO_NOTHING)
    id_criterio = models.ForeignKey(CriteriosMetrologicos, on_delete=models.PROTECT)
    valor = models.FloatField()

    def __str__(self):
        return str(self.cod_cer_cal)  # Convierte el objeto a una cadena antes de devolverlo



