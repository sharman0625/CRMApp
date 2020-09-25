
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('products', views.products),
    path('customers', views.customers),
]