from django.urls import path
from . import views

app_name = "listado"
          
urlpatterns = [
    path("", views.home, name="Home"),
]