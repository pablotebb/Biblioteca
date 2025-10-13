from django.urls import path
from . import views

app_name = "libros"

urlpatterns = [
    path("", views.home, name="Home"),
]