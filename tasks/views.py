from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def task_detail(request, task_id):
    #Bloque READ
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = CreateTaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form':form})
    else: 
        #Bloque UPDATE
        try:
            print(request.POST)
            task = get_object_or_404(Task, pk=task_id, user=request.user) 
            form = CreateTaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form':form, 'error': "Error al actualizar la tarea"})

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks':tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') 
    return render(request, 'tasks.html', {'tasks':tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form' : CreateTaskForm
        })
    else: 
        try:
            form = CreateTaskForm(request.POST)
            new_task = form.save(commit=False) 
            new_task.user = request.user 
            print(new_task) #Esto muestra los datos ingresados
            new_task.save()
            return redirect('tasks')
        except ValueError: 
            return render(request, 'create_task.html', {
                'form' : CreateTaskForm,
                'error' : "Por favor, ingrese datos validos"
            })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form' : AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None: 
            return render(request, 'signin.html', {
                'form' : AuthenticationForm, 
                'error' : 'Username or Password Incorrect!'
            })
        else: 
            login(request, user) 
            return redirect('tasks') 
          
@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'GET':
         return render(request, "signup.html", {
            'form' : UserCreationForm
        })
    else: 
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1']) 
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, "signup.html", {
                    'form' : UserCreationForm,
                    "error": "Username already exists!"
                })
        return render(request, "signup.html", {
                    'form' : UserCreationForm,
                    "error": "Password does not match!"
                })

def home(request):
    return render(request, "home.html")




        
    