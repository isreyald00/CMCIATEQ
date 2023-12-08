from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from .models import CustomUser

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'id': 'loginEmail',
                'type': 'email',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'nombre', 'apellido_p', 'apellido_m', 'group')