# myproject/urls.py

from django.contrib import admin
from django.urls import path
from myapp import views  # Импортируйте ваше приложение

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Настройте путь к вашему представлению
    path('add-category/', views.add_category, name='add_category'),
    path('api/categories/', views.get_categories, name='get_categories'),
    path('search_tasks/', views.search_tasks, name='search_tasks'),
]
