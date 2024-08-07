from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Task, Category

def index(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.due_date:
                task.due_date = None  # Ensure None is saved if no date is selected
            if not task.category:
                task.category = None  # Ensure None is saved if no category is selected
            task.save()
            return redirect('index')  # Redirect after saving
    else:
        form = TaskForm()

    # Fetch all tasks
    tasks = Task.objects.all()
    categories = Category.objects.all()

    # Fetch categories to map task category ids to category names
    category_map = {category.id: category.name for category in Category.objects.all()}

    # Attach category names to tasks
    tasks_with_category_names = []
    for task in tasks:
        category_name = category_map.get(int(task.category), 'Нет категории') if task.category else 'Нет категории'
        tasks_with_category_names.append({
            'description': task.description,
            'category': category_name,
            'due_date': task.due_date,
        })

    return render(request, 'main.html', {'form': form, 'tasks': tasks_with_category_names, 'categories': categories})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category

@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category_name = data.get('name')
        if category_name:
            Category.objects.create(name=category_name)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

from django.http import JsonResponse
from .models import Category

def get_categories(request):
    categories = Category.objects.all()
    data = list(categories.values('id', 'name'))  # Используем 'id' и 'name' для передачи данных
    return JsonResponse(data, safe=False)


from django.http import JsonResponse
from django.templatetags.static import static
from .models import Task
from django.db.models import Q


from django.http import JsonResponse
from django.templatetags.static import static
from .models import Task, Category
from django.db.models import Q

def search_tasks(request):
    query = request.GET.get('query', '').lower()

    tasks = Task.objects.filter(
        Q(description__icontains=query) |
        Q(category__icontains=query)
    )

    # Fetch categories to map task category ids to category names
    category_map = {str(category.id): category.name for category in Category.objects.all()}

    tasks_list = [{
        'description': task.description,
        'category': category_map.get(task.category, 'Нет категории') if task.category else 'Нет категории',
        'due_date': task.due_date.strftime("%d.%m.%Y %H:%M") if task.due_date else None,
        'complete_icon_url': static('img/complete.svg'),  # adjust the static URL path as needed
    } for task in tasks]

    return JsonResponse({'tasks': tasks_list})


