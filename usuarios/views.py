from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db import transaction

from django.conf import settings


from .forms import UserLoginForm, UserRegistrationForm

def is_admin_user(user):
    # Esta función verifica si el usuario actual pertenece al grupo "Admin".
    return user.groups.filter(name='Admin').exists()

def is_in_allowed_groups(user):
    allowed_groups = ['Admin', 'Capturista']  # Lista de nombres de grupos permitidos
    return user.groups.filter(name__in=allowed_groups).exists()

def user_not_logged_in(user):
    return not user.is_authenticated

def sinPermisoView(request):
    return render(request, "usuarios/sin_permiso.html")

@method_decorator(user_passes_test(user_not_logged_in, login_url=reverse_lazy('core:menuPrincipal')), name='dispatch')
class UserLoginView(LoginView):
    template_name = 'usuarios/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        messages.success(self.request, 'Has iniciado sesión correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Correo electrónico o contraseña inválida')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('core:menuPrincipal')
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('usuarios:login')

@method_decorator(user_passes_test(is_admin_user, login_url='usuarios:sinPermiso'), name='dispatch')
class UserRegistrationView(CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm  # El formulario que estás utilizando
    template_name = 'usuarios/register.html'  # Plantilla de registro

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            group = form.cleaned_data.get('group')
            user.groups.add(group)
            permissions = group.permissions.all()
            user.user_permissions.set(permissions)

            '''name = user.nombre
            email = user.email
            subject = "Confirmación de alta en Sistema de Control Metrológico"
            message = "Bienvenido a al sistema de control metrológico de CIATEQ"

            template = render_to_string('usuarios/email_template.html', {
                'name': name,
                'email': email,
                'message': message
            })

            email = EmailMessage(
                subject,
                template,
                settings.EMAIL_HOST_USER,
                ['18030229@itesa.edu.mx']
            )

            email.fail_silently = False
            #email.send()'''

            messages.success(self.request, 'Registro del usuario exitoso')
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:menuPrincipal')
