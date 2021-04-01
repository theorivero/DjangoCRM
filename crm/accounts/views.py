from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import *
from .filters import *


def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')

	context = {'form':form}
	
	return render(request, 'accounts/register.html', context)

def loginPage(request):
	context = {}
	return render(request, 'accounts/login.html', context)

def home(request):
	customers = Customer.objects.all()
	orders = Order.objects.all()

	delivered = Order.objects.filter(status='Delivered')
	pending = Order.objects.filter(status='Pending')

	context = {
		"customers" : customers,
		"orders" : orders,
		"delivered" : delivered,
		"pending" : pending

	}
	return render(request, 'accounts/dashboard.html', context)
	
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products': products})

def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()

	MyFilter = OrderFilter(request.GET, queryset=orders)
	orders = MyFilter.qs

	context = {'customer': customer, 'orders': orders, 'MyFilter':MyFilter}
	return render(request, 'accounts/customer.html', context)

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


def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == "POST":
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')




	context = {'form': form}

	return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):

	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {"item": order}
	return render(request, 'accounts/delete.html', context)



def createCustomer(request):
	form = CustomerForm()

	if request.method == "POST":
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context ={'form': form}
	return render(request, 'accounts/customer_form.html', context)

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

def deleteCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	if request.method == 'POST':
		customer.delete()
		return redirect('/')


	context = {'item': customer}
	return render(request, 'accounts/delete.html', context)


