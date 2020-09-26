
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.products, name='products'),
    path('customer/<str:pk>/', views.customers, name='customer'),
]