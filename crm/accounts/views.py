from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .filters import *
from .decorators import  *


@unauthenticated_user
def registerPage(request):	
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)

			Customer.objects.create(
				user = user,
    			name=user.username,
    			email= user.email
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')

	context = {'form':form}
	
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):	
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Username or password is incorect')

	context = {}
	return render(request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	customers = Customer.objects.all()
	orders = Order.objects.all().order_by('-date_created')[:5]
	count_orders = Order.objects.all().count() 
	delivered = Order.objects.filter(status='Delivered')
	pending = Order.objects.filter(status='Pending')

	context = {
		"customers" : customers,
		"orders" : orders,
		"delivered" : delivered,
		"pending" : pending,
		"count_orders" : count_orders

	}
	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')	
@allowed_users(allowed_roles=['customer'])
def userPage(request):

	orders = request.user.customer.order_set.all()

	count_orders = orders.count() 
	delivered = orders.filter(status='Delivered')
	pending = orders.filter(status='Pending')

	context = {
		"orders" : orders,	
		"delivered" : delivered,
		"pending" : pending,
		"count_orders" : count_orders	
	}

	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')	
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()

	MyFilter = OrderFilter(request.GET, queryset=orders)
	orders = MyFilter.qs

	context = {'customer': customer, 'orders': orders, 'MyFilter':MyFilter}
	return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
	customer = Customer.objects.get(id=pk)
	#form = OrderForm(initial = {'customer': customer})
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	if request.method == "POST":
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset': formset}

	return render(request, 'accounts/order_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == "POST":
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')




	context = {'form': form}

	return render(request, 'accounts/single_order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createSingleOrder(request):
	form = OrderForm()

	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request, 'accounts/single_order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):

	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {"item": order}
	return render(request, 'accounts/delete.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
	form = CustomerForm()

	if request.method == "POST":
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context ={'form': form}
	return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	form = CustomerForm(instance=customer)
	if request.method == "POST":
		form = CustomerForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')

	context ={'form': form}
	return render(request, 'accounts/customer_form.html', context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def deleteCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	if request.method == 'POST':
		customer.delete()
		return redirect('/')


	context = {'item': customer}
	return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context = {"form": form}
	return render(request, 'accounts/account_settings.html', context)

