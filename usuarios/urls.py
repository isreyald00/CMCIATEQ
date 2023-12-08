from django.urls import path
from . import views
from .views import UserLoginView, UserRegistrationView

app_name='usuarios'
urlpatterns=[
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', UserRegistrationView.as_view(), name='registro'),
    path('sinPermiso/', views.sinPermisoView, name='sinPermiso'),
]