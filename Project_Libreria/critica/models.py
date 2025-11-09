from django.db import models
from libros.models import Libro
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Critica(models.Model):
   # Cambiamos a ForeignKey para permitir múltiples críticas por libro
   libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='criticas', null=True)
   usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='criticas', null=True)
   titulo = models.CharField(max_length=200, null=True)
   contenido = models.TextField(null=True)
   puntuacion = models.IntegerField(
      validators=[MinValueValidator(1), MaxValueValidator(5)],
      null=True
   )
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   
   class Meta:
      verbose_name = "crítica"
      verbose_name_plural = "críticas"
      ordering = ['-created']

   def __str__(self):
     return f"{self.titulo} ({self.libro.titulo})"
