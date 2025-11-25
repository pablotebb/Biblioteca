from django.urls import path
from . import views

app_name = 'libro'

urlpatterns = [
    path("", views.libro_view, name="libros"),
    path('editar/<int:pk>/', views.editar_libro, name='editar_libro'),
    path('borrar/<int:pk>/', views.borrar_libro, name='borrar_libro'),
]
