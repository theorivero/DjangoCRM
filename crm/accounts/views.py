from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *

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
	context = {'customer': customer, 'orders': orders}
	return render(request, 'accounts/customer.html', context)

def createOrder(request):

	form = OrderForm()
	if request.method == "POST":
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form': form}

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