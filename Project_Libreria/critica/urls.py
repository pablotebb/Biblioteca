from django.urls import path
from . import views

app_name = "critica"

urlpatterns = [
    path('', views.critica_view, name='critica'),
    path('editar/<int:pk>/', views.editar_critica, name='editar_critica'),
    path('borrar/<int:pk>/', views.borrar_critica, name='borrar_critica'),
]