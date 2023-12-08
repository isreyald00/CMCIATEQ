
# Importa las clases necesarias de Django
from django.forms import ModelForm
from django import forms

from .models import EspecificacionMetrologia, CriteriosMetrologicos
from inventario.models import Equipo

class EspecificacionMetrologicaForm(ModelForm):
    class Meta:
        model = EspecificacionMetrologia  # Asocia el formulario al modelo "EspecificacionMetrologia"
        fields = '__all__'  # Incluye todos los campos del modelo en el formulario
        exclude = ['id_equipo']
        labels ={
            'res_unidades': 'Resolución de unidades',
            'unidades': 'Unidad',
            'intervalo_medicion_unidades': 'Intervalo de medición de unidades'
        }
    def __init__(self, *args, **kwargs):
        deshabilitar_criterio = kwargs.pop('deshabilitar_criterio', False)
        super().__init__(*args, **kwargs)

        if deshabilitar_criterio:
            # Cambia el widget a CharField y hazlo de solo lectura
            self.fields['id_criterio'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
    

class DetalleControlMetroForm(ModelForm):
    class Meta:
        model = CriteriosMetrologicos
        fields = ['id_criterio', 'valor_esperado', 'id_unidad_criterio', 'rango']

class IncertidumbreForm(ModelForm):
    class Meta:
        model = CriteriosMetrologicos
        fields = ['valor_esperado', 'id_unidad_criterio', 'rango']
    

