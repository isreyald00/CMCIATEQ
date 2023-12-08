# manual_task.py

import os
from celery import Celery
from calibracion.tasks import cambiar_estatus

# Configura Celery después de establecer la variable de entorno
app = Celery('ControlMetrologicoCIATEQ')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Asegúrate de descubrir las tareas automáticamente
app.autodiscover_tasks()

# Establece la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ControlMetrologicoCIATEQ.settings")

# Llama a la tarea manualmente
result = cambiar_estatus.apply_async()

# Espera a que la tarea termine y obtén el resultado
result.get()

