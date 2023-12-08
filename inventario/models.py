from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import request
import qrcode
from io import BytesIO
from django.core.files import File


class DireccionEspecialidad(models.Model):
    id = models.CharField(max_length=4, primary_key= True)
    nombre = models.CharField(max_length=40)

    def __str__(self):
        return str(self.nombre)  # Convierte el objeto a una cadena antes de devolverlo

class Sede(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    nombre = models.CharField(max_length=15)

    def __str__(self):
        return str(self.nombre)  # Convierte el objeto a una cadena antes de devolverlo

class Magnitud(models.Model):
    id = models.CharField(max_length=1, primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return str(self.nombre)  # Convierte el objeto a una cadena antes de devolverlo

class Clasificacion(models.Model):
    id = models.CharField(max_length=1, primary_key=True)
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return str(self.nombre)  # Convierte el objeto a una cadena antes de devolverlo

class Equipo(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    activo_fijo = models.CharField(max_length=10, null=True, blank=True)
    id_direccion_esp = models.ForeignKey(DireccionEspecialidad, on_delete=models.PROTECT, verbose_name="Direccion de especialidad")
    id_sede = models.ForeignKey(Sede, on_delete=models.PROTECT)
    id_responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='responsable_equipo')
    nombre_eq = models.CharField(max_length=100)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=30)
    n_serie = models.CharField(max_length=30)
    id_magnitud = models.ForeignKey(Magnitud, on_delete=models.PROTECT)
    id_clasificacion = models.ForeignKey(Clasificacion, on_delete=models.PROTECT)
    id_responsable_alta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='responsable_alta')
    accesorios = models.CharField(max_length=100, null= True, blank=True)
    codigo_qr = models.ImageField(upload_to='imgs/inventario/QR/', null=True, blank=True)
    imagen = models.ImageField(upload_to='imgs/inventario/equipos/', null=True, blank=True)
    estatus = models.CharField(max_length=10, default="Activo")
    fecha_alta = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)  # Convierte el objeto a una cadena antes de devolverlo
    
    def save(self, *args, **kwargs):
        if not self.id:

            id_direccion_esp = self.id_direccion_esp.id
            id_magnitud = self.id_magnitud.id
            id_clasificacion = self.id_clasificacion.id
            id_sede = self.id_sede.id

            registros_similares = Equipo.objects.filter(
                id_direccion_esp=id_direccion_esp,
                id_magnitud=id_magnitud,
                id_clasificacion=id_clasificacion,
                id_sede=id_sede
            )

            max_consecutive = registros_similares.aggregate(models.Max('id'))
            if max_consecutive['id__max']:
                parts = max_consecutive['id__max'].split('-')
                consecutivo_anterior = int(parts[2])
                nuevo_consecutivo = consecutivo_anterior + 1
                nuevo_consecutivo_str = str(nuevo_consecutivo).zfill(4)
                nuevo_id = f'{id_direccion_esp}-{id_magnitud}-{nuevo_consecutivo_str}-{id_clasificacion}-{id_sede}'
                self.id = nuevo_id
            else:
                self.id = f'{id_direccion_esp}-{id_magnitud}-0001-{id_clasificacion}-{id_sede}'

        if not self.codigo_qr:
            # Crea la URL para el código QR (ajusta la URL según tus necesidades)
            qr_url = f'{self.id}'

            # Crea el código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_url)
            qr.make(fit=True)

            # Crea una imagen del código QR
            img = qr.make_image(fill_color="black", back_color="white")

            # Guarda la imagen en el campo 'codigo_qr' del equipo
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            self.codigo_qr.save(f'{self.id}.png', File(buffer), save=False)

        if self.imagen:
            # Genera un nuevo nombre único para el archivo
            extension = self.imagen.name.split('.')[-1]  # Obtiene la extensión del archivo
            new_name = f'{self.id}.{extension}'
            
            # Asigna el nuevo nombre al archivo de imagen
            self.imagen.name = new_name

        super().save(*args, **kwargs)

class Baja (models.Model):
    id_equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE)
    motivos = models.TextField(blank=False)
    id_aprueba = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id_equipo)  # Convierte el objeto a una cadena antes de devolverlo


class DetalleDocs (models.Model):
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    url = models.FileField(upload_to='docs/inventario/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.url:
                print("Entro a asignar nuevo nombre al archivo")
                # Genera un nuevo nombre único para el archivo
                new_name = f'{self.id_equipo}_{self.url.name}'
                
                # Asigna el nuevo nombre al archivo de imagen
                self.url.name = new_name
        super().save(*args, **kwargs)


