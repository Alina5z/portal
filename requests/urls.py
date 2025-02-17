from django.urls import path
from . import views
from django.urls import path
from .views import request_list, get_resolved_count

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('create/', views.request_create, name='request_create'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('get_resolved_count/', get_resolved_count, name='get_resolved_count'),
]
