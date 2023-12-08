from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from inventario.models import Equipo
from django.conf import settings
from datetime import date, timedelta



class EspecificacionMantenimiento(models.Model):
    class OpcionesPeriodo(models.TextChoices):
        MESES = 'meses', 'meses'
        HORAS = 'horas', 'horas'

    id_equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, null=False, blank=False, primary_key=True)
    periodo = models.IntegerField(null=False, blank=False)
    tipo_periodo = models.CharField(max_length=10,choices=OpcionesPeriodo.choices,default=OpcionesPeriodo.MESES,)
    tiempo_uso = models.FloatField(null=True, blank=True)
    ultima = models.DateField(null=True, blank = True)
    proxima = models.DateField(null = True, blank= True)
    estado = models.CharField(max_length=10,default="Pendiente",)
    comentario = models.TextField(null=True, blank=True)

    def clean(self):
        if self.periodo < 1:
            raise ValidationError({'periodo': 'El valor del Periodo debe ser mayor que 0.'})
        if self.ultima > date.today():
            raise ValidationError({'ultima': 'La fecha de último mantenimiento debe ser anterior a la fecha actual.'})
        if self.proxima < date.today():
            raise ValidationError({'proxima': 'La fecha de próximo mantenimiento debe ser posterior a la fecha actual.'})
        return super().clean()

    def __str__(self):
        return str(self.id_equipo)

    
        

class DetalleMantenimientoInterno(models.Model):
    num_folio = models.AutoField(primary_key=True)
    id_especificacion_mant = models.ForeignKey(EspecificacionMantenimiento, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    id_responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='responsable_mant')
    tipo_mant  = models.CharField(max_length=10)
    comentario = models.TextField(null=True, blank=True)
    evidencia = models.ImageField(upload_to='imgs/mantenimiento/evidencias/interno', null=True, blank=True)
    id_responsable_cap = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='responsable_captura', null=True)

    def save(self, *args, **kwargs):
        if self.evidencia:
            # Genera un nuevo nombre único para el archivo
            extension = self.evidencia.name.split('.')[-1]  # Obtiene la extensión del archivo
            new_name = f'{self.num_folio}.{extension}'
            
            # Asigna el nuevo nombre al archivo de imagen
            self.evidencia.name = new_name

        super().save(*args, **kwargs)

    def clean(self):
        if self.fecha > date.today():
            raise ValidationError({'fecha': 'La fecha de mantenimiento no debe ser posterior a la fecha actual.'})
        return super().clean()

    def __str__(self):
        return str(self.num_folio)

class DetalleMantenimientoExterno(models.Model):
    num_folio = models.AutoField(primary_key=True)
    id_especificacion_mant = models.ForeignKey(EspecificacionMantenimiento, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    proveedor = models.CharField(max_length=100, null=False, blank=False)
    tipo_mant  = models.CharField(max_length=10)
    comentario = models.TextField(null=True, blank=True)
    evidencia = models.ImageField(upload_to='imgs/mantenimiento/evidencias/externo', null=True, blank=True)
    id_responsable_cap = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

    def save(self, *args, **kwargs):
        if self.evidencia:
            # Genera un nuevo nombre único para el archivo
            extension = self.evidencia.name.split('.')[-1]  # Obtiene la extensión del archivo
            new_name = f'{self.num_folio}.{extension}'
            
            # Asigna el nuevo nombre al archivo de imagen
            self.evidencia.name = new_name

        super().save(*args, **kwargs)

    def clean(self):
        if self.fecha > date.today():
            raise ValidationError({'fecha': 'La fecha de mantenimiento no debe ser posterior a la fecha actual.'})
        return super().clean()

    def __str__(self):
        return str(self.num_folio)