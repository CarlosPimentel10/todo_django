from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from .models import Task
from .forms import TaskForm


def addTask(request):
    form = TaskForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            task = form.cleaned_data['task']
            Task.objects.create(task=task)
            return redirect('home')
        else:
            messages.error(request, 'Task cannot be blank.')

    context = {'form': form}
    return render(request, 'home.html', context=context)


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
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task.task = form.cleaned_data['task']
            task.save()
            return redirect('home')
        else:
            messages.error(request, 'Task cannot be blank.')
    else:
        form = TaskForm(initial={'task': task.task})

    context = {'form': form, 'get_task': task}
    return render(request, 'edit_task.html', context)


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        confirmed = request.POST.get('confirmed')

        if confirmed == 'true':
            task.delete()
            messages.success(request, 'Task deleted successfully.')
        else:
            messages.info(request, 'Deletion canceled.')

        return redirect('home')

    context = {'task': task}
    return render(request, 'delete_task.html', context)



