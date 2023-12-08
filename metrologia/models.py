from django.db import models
from django.core.exceptions import ValidationError

from inventario.models import Equipo, Magnitud

class Unidad(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=35)
    id_magnitud = models.ForeignKey(Magnitud, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)  # Convierte el objeto a una cadena antes de devolverlo

class Criterio (models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    def __str__(self):
        return str(self.id)  # Convierte el objeto a una cadena antes de devolverlo

class EspecificacionMetrologia (models.Model):
    id_equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, primary_key=True)
    res_unidades = models.CharField(max_length=25, null=True, blank=True)
    unidades = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    intervalo_medicion_unidades = models.CharField(max_length=30)

    def __str__(self):
        return str(self.id_equipo)  # Convierte el objeto a una cadena antes de devolverlo

class CriteriosMetrologicos(models.Model): #Se especifican los criterios a considerar en cada herramienta
    class Opciones(models.TextChoices):
        MAX = 'Max', 'Max'
        MIN = 'Min', 'Min'
        PLUS_MINUS = '±', '±'
        EQUAL = '=', '='
    id_controlMetro = models.ForeignKey(EspecificacionMetrologia, on_delete=models.CASCADE)
    rango = models.CharField(max_length=10,choices=Opciones.choices,)
    id_criterio = models.CharField(max_length=20, null=False, blank=False)
    valor_esperado = models.FloatField(null=False, blank=False)
    id_unidad_criterio = models.ForeignKey(Unidad, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id_criterio)  # Convierte el objeto a una cadena antes de devolverlo



