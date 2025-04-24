from django.contrib import admin
from .models import Task #Con esto Task tiene acceso al panel de admin

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", ) 

# Register your models here.
admin.site.register(Task, TaskAdmin)




