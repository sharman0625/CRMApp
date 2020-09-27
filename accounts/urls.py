
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    
    path('', views.home, name='home'),
    path('products', views.products, name='products'),
    path('customer/<str:pk>/', views.customers, name='customer'),
    
    path('create_order/<str:pk>/', views.creatOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
]