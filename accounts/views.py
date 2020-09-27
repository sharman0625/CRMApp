from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import OrderForm

# Create your views here.

def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all().order_by('-date_created')

    total_orders = orders.count()
    delivered_orders = orders.filter(status="Delivered").count()
    pending_orders = orders.filter(status="Pending").count()
    outfordelivery_orders = orders.filter(status="Out for Delivery").count()

    context = {
        'customers' :customers, 
        'orders' :orders, 
        'total_orders' :total_orders, 
        'delivered_orders' :delivered_orders, 
        'pending_orders' :pending_orders,
        'outfordelivery_orders' : outfordelivery_orders
    }

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'accounts/product.html', context)


def customers(request, pk):
    customer = Customer.objects.get(pk=pk)
    orders = customer.order_set.all()
    context = {
        'customer' : customer,
        'orders' : orders
    }
    return render(request, 'accounts/customer.html', context)


def creatOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form' : form
    }
    return render(request, "accounts/order_form.html", context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method=='POST':
        form = OrderForm(request.POST, instance=order)
        form.save()
        return redirect('/')
    context = {
        'form' : form
    }
    return render(request, "accounts/order_form.html", context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    context = {
        'order' : order
    }
    return render(request, 'accounts/delete.html', context)
