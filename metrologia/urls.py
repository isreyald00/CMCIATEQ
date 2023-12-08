from django.urls import path
from . import views

app_name='metrologia'
urlpatterns=[
    #ejemplo: metrologia/
    path('', views.metrologiaView, name='metrologia'),

    #ejemplo: metrologia/registrarEspecificacionMetrologica/
    #path('registrarEspecificacionMetrologica/', views.AgregarEspecificacionMetrologicaView, name='registrarEsp'),

    #ejemplo: metrologia/agregarIncertidumbre/
    path('agregarIncertidumbre/<str:equipo>', views.AgregarIncertidumbreView.as_view(), name='agregarIncer'),

    #ejemplo: metrologia/registrarEspecificacionMetrologica/(id_equipo)/(cal)/(ver)
    path('registrarEspecificacionMetrologica/<str:equipo>/<str:cal>/<str:ver>', views.AgregarEspecificacionMetrologicaView.as_view(), name='registrarEsp'),
]