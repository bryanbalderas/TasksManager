from django.contrib import admin
from .models import Task, Estatus, Departamento
# Register your models here.

admin.site.register(Task)
admin.site.register(Estatus)
admin.site.register(Departamento)