from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from todo.forms import TaskForm


def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'base.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create.html', {'form': form})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit.html', {'form': form, 'task': task})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'delete_confirm.html', {'task': task})


def task_toggle_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    order = [Task.Status.TODO, Task.Status.IN_PROGRESS, Task.Status.DONE]
    next_index = (order.index(task.status) + 1) % len(order)
    task.status = order[next_index]
    task.save()
    return redirect('task_list')