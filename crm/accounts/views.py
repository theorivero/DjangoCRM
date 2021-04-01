from django.shortcuts import render
from django.http import HttpResponse

from .models import *

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

def customer(request):
	return render(request, 'accounts/customer.html')
