# from django.forms import ModelForm
from django import forms
from .models import Task

# class CreateTaskForm(ModelForm):
class CreateTaskForm(forms.ModelForm):
    class Meta: 
    #pasamos el modelo en el cual va a estar basado el formulario
        model = Task
        fields = ['title','description','important']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Type A Title'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Type a description'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
        
        
        
        