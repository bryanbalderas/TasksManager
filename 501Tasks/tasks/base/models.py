from typing import Tuple
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Estatus(models.Model):
    title=models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.title
    

    
class Departamento(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.title
    


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    complete =models.BooleanField(default=False)
    create =models.DateTimeField(auto_now_add=True)
    creador = models.CharField(max_length=200,null=True)
    Estatus=models.ForeignKey(Estatus,on_delete=models.CASCADE,null=True,blank=True)
    Departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE,null=True)
    archivos=models.FileField(upload_to='documents/%Y/%m/%d',null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['complete']