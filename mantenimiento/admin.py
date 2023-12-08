from django.contrib import admin
from .models import EspecificacionMantenimiento, DetalleMantenimientoExterno, DetalleMantenimientoInterno

admin.site.register(EspecificacionMantenimiento)
admin.site.register(DetalleMantenimientoExterno)
admin.site.register(DetalleMantenimientoInterno)