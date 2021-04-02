from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .filters import *


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('/')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')

		context = {'form':form}
		
		return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('/')
	else:
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
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()

	MyFilter = OrderFilter(request.GET, queryset=orders)
	orders = MyFilter.qs

	context = {'customer': customer, 'orders': orders, 'MyFilter':MyFilter}
	return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
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
def deleteOrder(request, pk):

	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {"item": order}
	return render(request, 'accounts/delete.html', context)



@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	if request.method == 'POST':
		customer.delete()
		return redirect('/')


	context = {'item': customer}
	return render(request, 'accounts/delete.html', context)


