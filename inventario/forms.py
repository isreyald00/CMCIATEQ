
from django import forms
from .models import Equipo, Baja, DetalleDocs

class ModificarEquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__'

class DetalleDocsForm(forms.ModelForm):
    class Meta:
        model: DetalleDocs
        fields = ['url']

class AgregarEquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__' 
        exclude = ['id', 'id_responsable_alta','estatus', 'codigo_qr']

    necesita_cal = forms.ChoiceField(
        choices=[('Si', 'Sí'), ('No', 'No')],
        label='¿Necesita control de calibraciones?',
        required=True
    )
    necesita_ver = forms.ChoiceField(
        choices=[('Si', 'Sí'), ('No', 'No')],
        label='¿Necesita control de verificaciones?',
        required=True
    )      
    necesita_mant = forms.ChoiceField(
        choices=[('Si', 'Sí'), ('No', 'No')],
        label='¿Necesita control de mantenimiento?',
        required=True
    )

class BajaEquipoForm(forms.ModelForm):
    class Meta:
        model = Baja
        fields = '__all__'
        exclude = ['id_equipo', 'fecha']