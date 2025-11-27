from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Categoria(models.Model):
  nombre = models.CharField(max_length=50)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    verbose_name = "categoria"
    verbose_name_plural = "categorias"
    
  def __str__(self):
    return self.nombre
  
class Libro(models.Model):
  id_libros = models.ForeignKey(User, on_delete=models.CASCADE)
  isbn = models.CharField(max_length=20)
  autor = models.CharField(max_length=50)
  titulo = models.CharField(max_length=50)
  categoria = models.ManyToManyField(Categoria)
  contenido = models.TextField(max_length=200)
  imagen = models.ImageField(upload_to="libros", null=True, blank=True)
  leido = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    verbose_name = "libro"
    verbose_name_plural = "libros"
    
  def __str__(self):
    return self.titulo
