from django.contrib import admin
from .models import Critica

# Register your models here.

class CriticaAdmin(admin.ModelAdmin):
  readonly_fields = ("created", "updated")
  

admin.site.register(Critica, CriticaAdmin)
