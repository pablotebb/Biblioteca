from django.urls import path
from . import views

app_name = "critica"

urlpatterns = [
    path("", views.home, name="Home"),
]