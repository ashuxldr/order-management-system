# all import files below
from .forms import *
from .models import *
from .decorators import *
from .filters import OrderFilter
from django.contrib import messages
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# dashboard view function below


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'customers': customers,
               'orders': orders,
               'total_orders': total_orders,
               'total_customers': total_customers,
               'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


# about view function below

@login_required(login_url='login')
def about(request):
    return render(request, 'accounts/about.html')


# product view function below

@login_required(login_url='login')
@allowed_user(allowed_roles='admin')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


# customer view function below
@login_required(login_url='login')
@allowed_user(allowed_roles='admin')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'myFilter': myFilter,
    }
    return render(request, 'accounts/customer.html', context)


# create order view function below

@login_required(login_url='login')
@allowed_user(allowed_roles='admin')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/order_page.html', context)


# updateOrder view function below

@login_required(login_url='login')
@allowed_user(allowed_roles='admin')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'formset': form}
    return render(request, 'accounts/order_page.html', context)


# delete order view function below

@login_required(login_url='login')
@allowed_user(allowed_roles='admin')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'accounts/delete_order.html', context)


# Register Page view function below

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


# Login Page view function below

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)


# Logout view function below

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


# USER PAGE FUNCTION
@login_required(login_url='login')
@allowed_user(allowed_roles='customer')
def user(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending,
               }
    return render(request, 'accounts/user.html', context)


def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)
