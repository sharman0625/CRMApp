from django.shortcuts import render
from django.http import HttpResponse

from .models import *

# Create your views here.

def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    delivered_orders = orders.filter(status="Delivered").count()
    pending_orders = orders.filter(status="Pending").count()

    context = {
        'customers' :customers, 
        'orders' :orders, 
        'total_orders' :total_orders, 
        'delivered_orders' :delivered_orders, 
        'pending_orders' :pending_orders
    }

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'accounts/product.html', context)

def customers(request):
    return render(request, 'accounts/customer.html')
