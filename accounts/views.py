from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import OrderForm
from .filters import OrderFilter

# Create your views here.

def login(request):
    return render(request, 'accounts/login.html', context)

def register(request):
    form = UserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/register.html', context)

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

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer' : customer,
        'orders' : orders,
        'myFilter' : myFilter
    }
    return render(request, 'accounts/customer.html', context)


def creatOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=['product', 'status'], extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method=='POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset' : formset
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
