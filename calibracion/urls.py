from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "calibracion"
urlpatterns = [
    # ex: metrologia/calibracion/
    path("", views.CalibracionView.as_view(), name="calibracion"),

    # ex: metrologia/calibracion/historial
    path("historial/", views.HistorialCalibracionView.as_view(), name="historial"),

    # ex: metrologia/calibracion/modificarEspecificacion/(id de equipo)
    path("modificarEspecificacion/<str:pk>/", views.ModificarEspView.as_view(), name="modificarEsp"),

    # ex: /metrologia/calibracion/detalles/(id_equipo)
    path("detalles/<str:pk>/", views.DetallesCalView.as_view(), name="detalles"),

    # ex: metrologia/calibracion/nuevaCalibracion/(id de equipo)
    path("nuevaCalibracion/<str:pk>/", views.RegistrarCalibracionView, name="registrarCal"),

    # ex: metrologia/calibracion/registrarEspCal/
    #path("registrarEspCal/", views.AgregarEspCalView.as_view(), name="registrarEsp"),

    # ex: metrologia/calibracion/registrarEspCal/
    path("registrarEspCal/<str:equipo>/<str:ver>/", views.AgregarEspCalView.as_view(), name="registrarEsp"),

    # ex: metrologia/calibracion/generar_pdf/(id_equipo)
    path('generar_pdf/<str:pk>/<str:id>/', views.generar_pdf, name='generar_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)