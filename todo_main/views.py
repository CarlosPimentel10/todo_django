from django.shortcuts import render
from todo.models import Task

def home(request):
    tasks = Task.objects.filter(is_completed=False).order_by('-updated_at')
    task_completed = Task.objects.filter(is_completed=True).order_by('-updated_at')

    context = {
        'tasks': tasks,
        'task_completed': task_completed,
        }
    return render(request, 'home.html', context)