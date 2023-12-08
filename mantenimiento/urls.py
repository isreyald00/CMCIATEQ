from django.urls import path
from . import views

app_name = "mantenimiento"
urlpatterns = [
    # ex: mantenimiento/
    path("", views.MantenimientoView.as_view(), name="mantenimiento"),

    # ex: /mantenimiento/agregarEspecificacion/
    #path("agregarEspecificacion/", views.AgregarEspManView.as_view(), name="registrarEsp"),
    # ex: /mantenimiento/agregarEspecificacion/(id_equipo)/(cal)/(ver)
    path("agregarEspecificacion/<str:equipo>/<str:cal>/<str:ver>/", views.AgregarEspManView.as_view(), name="registrarEsp"),

    # ex: /mantenimiento/detallesEspecificacion/(id_equipo)
    path("detallesEspecificacion/<str:pk>/", views.DetallesEspView.as_view(), name="detalles"),

    # ex: /mantenimiento/detallesInterno/(id_equipo)
    path("detallesInterno/<str:pk>/", views.DetallesMantIntView.as_view(), name="detallesInt"),

    # ex: /mantenimiento/detallesExterno/(id_equipo)
    path("detallesExterno/<str:pk>/", views.DetallesMantExtView.as_view(), name="detallesExt"),

    # ex: mantenimiento/modificarEspecificacion/(id de equipo)
    path("modificarEspecificacion/<str:pk>/", views.ModificarEspView.as_view(), name="modificarEsp"),

    # ex: mantenimiento/registrarInterno/(id de equipo)
    path("registrarInterno/<str:equipo>/", views.RegistrarMantIntView.as_view(), name="registrarInterno"),

    # ex: mantenimiento/registrarExterno/(id de equipo)
    path("registrarExterno/<str:equipo>/", views.RegistrarMantExtView.as_view(), name="registrarExterno"),

    #ejemplo: mantenimiento/historial/
    path('historial/', views.HistorialMantView, name='historial'),

    # ex: metrologia/mantenimiento/generar_pdf/(id_equipo)
    path('generar_pdf/<str:tipo>/<str:pk>/<str:id>/', views.generar_pdf, name='generar_pdf'),
]