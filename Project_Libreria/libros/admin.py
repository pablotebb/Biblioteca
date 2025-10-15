from django.contrib import admin
from .models import Categoria, Libro

# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
  readonly_fields = ("created", "updated")
  
class LibroAdmin(admin.ModelAdmin):
  readonly_fields = ("created", "updated")

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Libro, LibroAdmin)
