from django.urls import path
from . import views

app_name = "verificacion"
urlpatterns = [
    # ex: metrologia/verificacion/
    path("", views.VerificacionView.as_view(), name="verificacion"),

    # ex: metrologia/verificacion/historial
    path("historial/", views.HistorialVerificacionView.as_view(), name="historial"),

    # ex: metrologia/verificacion/modificarEspecificacion/(id de equipo)
    #path("modificarEspecificacion/<str:pk>/", views.ModificarEspView.as_view(), name="modificarEsp"),

    # ex: /metrologia/verificacion/detalles/(id_equipo)
    path("detalles/<str:pk>/", views.DetallesVerView.as_view(), name="detalles"),

    # ex: metrologia/verificacion/nuevaVerificacion/(id de equipo)
    path("nuevaVerificacion/<str:pk>/", views.RegistrarVerificacionView.as_view(), name="registrarVer"),

    # ex: /metrologia/verificacion/registrarEspVer/
    #path("registrarEspVer/", views.AgregarEspVerView.as_view(), name="registrarEsp"),

    # ex: /metrologia/verificacion/registrarEspVer/(id_equipo)
    path("registrarEspVer/<str:equipo>/", views.AgregarEspVerView.as_view(), name="registrarEsp"),

    # ex: metrologia/verificacion/generar_pdf/(id_equipo)
    path('generar_pdf/<str:id>/<str:pk>/<str:error>/', views.generar_pdf, name='generar_pdf'),

    # ex: metrologia/verificacion/modificarEspecificacion/(id de equipo)
    path("modificarEspecificacion/<str:pk>/", views.ModificarEspView.as_view(), name="modificarEsp"),
]