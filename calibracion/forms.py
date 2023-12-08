from django import forms
from .models import EspecificacionCalibracion, Calibracion, CriteriosCalibracion
from inventario.models import Equipo

class RegistrarEspCalForm(forms.ModelForm):
    class Meta:
        model = EspecificacionCalibracion
        fields = ['periodo']


class CalibracionForm(forms.ModelForm):
    class Meta:
        model = Calibracion  
        fields = '__all__'  
        exclude = ['resp_cap', 'fecha_cap', 'dictamen']
        widgets = {
            'id_especificacion': forms.HiddenInput(),
            'fecha': forms.DateInput(attrs={'type': 'date'}),

        }
    doc = forms.FileField(
        label='Archivo Adjunto',
    )

class CriteriosCalibracionForm(forms.ModelForm):
    class Meta:
        model = CriteriosCalibracion
        fields = ['id_criterio', 'valor']
        widgets = {
            'id_criterio': forms.HiddenInput()
        }

class ModificarEspForm(forms.ModelForm):
    class Meta:
        model = EspecificacionCalibracion
        fields = ['periodo']
        
