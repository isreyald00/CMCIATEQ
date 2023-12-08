from django.urls import path

from . import views

app_name = "inventario"
urlpatterns = [
    # ex: inventarioGral/
    path("", views.InventarioGralView.as_view(), name="inventarioGral"),

    # ex: inventarioGral/detalles/(id de equipo)
    path("detallesEquipo/<str:pk>/", views.DetallesView.as_view(), name="detalles"),

    # ex: inventarioGral/modificarEquipo/(id de equipo)
    path("modificarEquipo/<str:pk>/", views.ModificarEquipoView.as_view(), name="modificar"),

    # ex: inventarioGral/agregarEquipo/
    path("agregarEquipo/", views.AgregarEquipoView.as_view(), name="agregar"),

    # ex: inventarioGral/bajaEquipo/(id_equipo)
    path("bajaEquipo/<str:equipo>/", views.BajaEquipoView.as_view(), name="baja"),

    #ex: inventarioGral/documentos/(id_equipo)
    path("documentos/<str:equipo>/", views.DocsView.as_view(), name="documentos"),

    # ex: metrologia/verificacion/generar_pdf/(id_equipo)
    path('generar_pdf/<str:pk>/', views.generar_pdf, name='generar_pdf'),
]