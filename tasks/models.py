from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Task(models.Model): #"models.Model" para que Django pueda crear tabla Tasks
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True) #blank=True permite decir que es opcional para el administrador pero para la bd el null=True significa que sí se debe ingresar este dato 
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.title + ' - by ' + self.user.username
