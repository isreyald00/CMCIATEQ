from django.contrib import admin
from .models import EspecificacionCalibracion, Calibracion, CriteriosCalibracion

admin.site.register(EspecificacionCalibracion)
admin.site.register(Calibracion)
admin.site.register(CriteriosCalibracion)