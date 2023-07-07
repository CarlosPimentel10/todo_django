from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from .models import Task


def addTask(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        if task:
            Task.objects.create(task=task)
        else:
            messages.error(request, 'Task cannot be blank.')  # Display error messag
    return redirect('home')

def mark_as_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = True
    task.save(update_fields=['is_completed']) # performance optimization
    return redirect('home')

def mark_as_undone(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = False
    task.save(update_fields=['is_completed']) 
    return redirect('home')

def edit_task(request, pk):
    get_task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        # Handle POST request
        new_task = request.POST.get('task')
        
        if new_task:
            get_task.task = new_task
            get_task.save()
            return redirect('home')
        else:
            messages.error(request, 'Task cannot be blank.')  # Display error messag
            return redirect('edit_task', pk=pk)
    else:
        context = {
            'get_task': get_task,
            }
        
        return render(request, 'edit_task.html', context)


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        confirmed = request.POST.get('confirmed')
        if confirmed == True:
            task.delete()
            messages.success(request, 'Task deleted successfully.')
        else:
            messages.info(request, 'Deletion canceled.')

            return redirect('home')
    context = {
        'task':task,
        }
    return render(request, 'delete_task.html', context)