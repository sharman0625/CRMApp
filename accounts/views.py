from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            Customer.objects.create(user=user,)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Successfully created : '+username)
            return redirect('login')
    context = {
        'form' : form
    }
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Useranem OR Password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    
    total_orders = orders.count()
    delivered_orders = orders.filter(status="Delivered").count()
    pending_orders = orders.filter(status="Pending").count()
    outfordelivery_orders = orders.filter(status="Out for Delivery").count()

    context = {
        'orders' : orders,
        'total_orders' : total_orders,
        'delivered_orders' : delivered_orders,
        'pending_orders' : pending_orders,
        'outfordelivery_orders' : outfordelivery_orders
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def products(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'accounts/product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    context = {
        'order' : order
    }
    return render(request, 'accounts/delete.html', context)
