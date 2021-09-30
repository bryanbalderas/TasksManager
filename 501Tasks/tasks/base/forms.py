from django import forms
from django.forms import fields
from .models import Task

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Task
        fields=['archivos']
