from django import forms
from .models import EspecificacionVerificacion,Verificacion
from inventario.models import Equipo


class RegistrarEspVerForm(forms.ModelForm):
    class Meta:
        model = EspecificacionVerificacion
        fields = ['periodo']  

class VerificacionForm(forms.ModelForm):
    class Meta:
        model = Verificacion
        fields = '__all__'
        exclude = ['id_verificacion', 'dictamen']

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

'''class ModificarEspForm(forms.ModelForm):
    class Meta:
        model = EspecificacionVerificacion
        fields = '__all__'
    id_equipo = forms.CharField(
        widget=forms.TextInput(attrs={'readonly' : 'readonly'})
    )'''

class ModificarEspForm(forms.ModelForm):
    class Meta:
        model = EspecificacionVerificacion
        fields = ['periodo']