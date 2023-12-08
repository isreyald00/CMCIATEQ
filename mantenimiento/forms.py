from django import forms
from .models import EspecificacionMantenimiento, DetalleMantenimientoExterno, DetalleMantenimientoInterno
from inventario.models import   Equipo

class RegistrarEspManForm(forms.ModelForm):
    class Meta:
        model = EspecificacionMantenimiento
        fields = ['periodo', 'tipo_periodo', 'comentario']

class ModificarEspForm(forms.ModelForm):
    class Meta:
        model = EspecificacionMantenimiento
        fields = ['periodo', 'tipo_periodo', 'comentario']

class RegistrarMantIntForm(forms.ModelForm):
    class Meta:
        model = DetalleMantenimientoInterno
        fields = '__all__'  # Incluye todos los campos del modelo en el formulario
        exclude = ['num_folio']
        widgets = {
            'id_especificacion_mant': forms.TextInput(attrs={'readonly':True}),
            'id_responsable_cap': forms.HiddenInput(),
            'id_especificacion_mant': forms.HiddenInput(),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
    
    OPCIONES_TIPO_MANTENIMIENTO = (
        ('Preventivo', 'Preventivo'),
        ('Correctivo', 'Correctivo'),
    )
    tipo_mant = forms.ChoiceField(choices=OPCIONES_TIPO_MANTENIMIENTO, widget=forms.Select())

class RegistrarMantExtForm(forms.ModelForm):
    class Meta:
        model = DetalleMantenimientoExterno
        fields = '__all__'
        exclude = ['num_folio']
        widgets = {
            'id_especificacion_mant': forms.TextInput(attrs={'readonly':True}),
            'id_responsable_cap': forms.HiddenInput(),
            'id_especificacion_mant': forms.HiddenInput(),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    OPCIONES_TIPO_MANTENIMIENTO = (
        ('Preventivo', 'Preventivo'),
        ('Correctivo', 'Correctivo'),
    )
    tipo_mant = forms.ChoiceField(choices=OPCIONES_TIPO_MANTENIMIENTO, widget=forms.Select())