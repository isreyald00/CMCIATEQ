from django.urls import path
from . import views

app_name = "calendario"
urlpatterns = [
    # ex: calendario/
    path("", views.CalendarioView.as_view(), name="calendario"),
]