from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def more_priority_sort(task):
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    return (priority_order.get(task.priority, 3), -task.id)

def task_list(request):
    filter_criteria = request.GET.get('filter', 'newest')

    if filter_criteria == 'completed':
        tasks = Task.objects.filter(completed=True).order_by('-id')
    elif filter_criteria == 'uncompleted':
        tasks = Task.objects.filter(completed=False).order_by('-id')
    elif filter_criteria == 'more_priority':
        tasks = sorted(Task.objects.all(), key=more_priority_sort)
    else:
        tasks = Task.objects.all().order_by('-id')
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo_app/add_task.html', {'form': form})

def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('task_list')

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'todo_app/edit_task.html', {'form': form})

