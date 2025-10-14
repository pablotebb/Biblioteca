from django.db import models
from libros.models import Libro

# Create your models here.

class Critica(models.Model):
   id_libros = models.ForeignKey(Libro, on_delete=models.CASCADE)
   contenido = models.CharField(max_length=50)
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now_add=True)
   
   class Meta:
    verbose_name = "crítica"
    verbose_name_plural = "críticas"
    
 
