from django.db import models
from datetime import timedelta, date

from django.forms import ValidationError

from inventario.models import Equipo
from metrologia.models import CriteriosMetrologicos
from usuarios.models import CustomUser

class EspecificacionVerificacion(models.Model):
    id_equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, primary_key=True)
    periodo = models.IntegerField(null=False, blank= False)
    ultima = models.DateField(null=True, blank= True)
    proxima = models.DateField(null=True, blank= True)
    estatus = models.CharField(max_length=20, null=False, blank= False, default="Pendiente")

    def clean(self):
        if self.periodo < 1:
            raise ValidationError({'periodo': 'El valor del Periodo debe ser mayor que 0.'})
        if self.ultima and self.ultima > date.today():
            raise ValidationError({'ultima': 'La fecha de última verificación debe ser anterior a la fecha actual.'})
        if self.proxima and self.proxima < date.today():
            raise ValidationError({'proxima': 'La fecha de próxima verificación debe ser posterior a la fecha actual.'})
        return super().clean()

    def __str__(self):
        return str(self.id_equipo)

class Verificacion(models.Model):
    num_informe = models.AutoField(primary_key=True) 
    id_verificacion = models.ForeignKey(EspecificacionVerificacion, on_delete=models.CASCADE)
    fecha = models.DateField(null=False, blank=False)
    id_responsable = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='responsable_verificacion')
    id_patron = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING, null=False, blank=False)
    puntoVer1 = models.FloatField(null=True, blank=False)
    puntoVer2 = models.FloatField(null=True, blank=False)
    puntoVer3 = models.FloatField(null=True, blank=False)
    puntoVer4 = models.FloatField(null=True, blank=False)
    puntoVer5 = models.FloatField(null=True, blank=False)
    lecEq1 = models.FloatField(null=True, blank=False)
    lecEq2 = models.FloatField(null=True, blank=False)
    lecEq3 = models.FloatField(null=True, blank=False)
    lecEq4 = models.FloatField(null=True, blank=False)
    lecEq5 = models.FloatField(null=True, blank=False)
    lecPatron1 = models.FloatField(null=True, blank=False)
    lecPatron2 = models.FloatField(null=True, blank=False)
    lecPatron3 = models.FloatField(null=True, blank=False)
    lecPatron4 = models.FloatField(null=True, blank=False)
    lecPatron5 = models.FloatField(null=True, blank=False)
    errorVer1 = models.FloatField(null=True, blank=False)
    errorVer2 = models.FloatField(null=True, blank=False)
    errorVer3 = models.FloatField(null=True, blank=False)
    errorVer4 = models.FloatField(null=True, blank=False)
    errorVer5 = models.FloatField(null=True, blank=False)
    dictamen = models.CharField(max_length=11, null=False, blank=False)
    doc = models.FileField(upload_to='docs/verificacion/', null=True, blank=True)
    id_aprobación = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='aprueba_verificacion')

    def clean(self):
        if self.fecha > date.today():
            raise ValidationError({'fecha': 'La fecha de verificación no debe ser posterior a la fecha actual.'})
        return super().clean()

    def __str__(self):
        return self.num_informe

