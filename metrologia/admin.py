from django.contrib import admin
from .models import Unidad, Criterio, EspecificacionMetrologia, CriteriosMetrologicos

admin.site.register(Unidad)
admin.site.register(Criterio)
admin.site.register(EspecificacionMetrologia)
admin.site.register(CriteriosMetrologicos)