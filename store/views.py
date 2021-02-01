from django.shortcuts import render
from .models import	*
from . utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse

import datetime
import json
# Create your views here.

def contact(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	categories = Category.objects.all()

	context = {'items' :items, 'order':order,  'cartItems':cartItems , 'categories':categories}
	return render(request, 'store/contact.html', context)
def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.all()


	manufacturers = Manufacturer.objects.all()
	categories = Category.objects.all()


	context = {'products':products, 'cartItems': cartItems,'items' :items, 'order':order, 'manufacturers': manufacturers, 'categories':categories}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	categories = Category.objects.all()
				
	context = {'items' :items, 'order':order, 'cartItems':cartItems, 'categories':categories}
	print(context['cartItems'])


	return render(request, 'store/cart.html', context)


def checkout(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	categories = Category.objects.all()

	context = {'items' :items, 'order':order,  'cartItems':cartItems, 'categories':categories}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
		data = json.loads(request.body)
		productId = data['productId']
		action = data['action']

		print('Action:', action)
		print('ID:', productId)

		customer = request.user.customer
		product = Product.objects.get(id=productId)
		order, created = Order.objects.get_or_create(customer=customer,complete=False)

		orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

		if action == 'add':
			orderItem.quantity = (orderItem.quantity + 1)
		elif action == 'remove':	
			orderItem.quantity = (orderItem.quantity - 1)
		elif action == 'delete':	
			orderItem.quantity = 0
		orderItem.save()
		
		if orderItem.quantity <= 0:
			orderItem.delete()	

		return JsonResponse('Item was added', safe=False)	


#from django.views.decorators.csrf import csrf_exempt 

#@csrf_exempt
def processOrder(request):
	print('data',request.body)
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		
		
	
	else:
		customer, order =  guestOrder(request, data)
	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_grand_total):
			order.complete = True
	order.save()

	if order.needs_shipping == True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address1'],
			address_line_2=data['shipping']['address2'],
			country=data['shipping']['country'],
			postcode=data['shipping']['post'],

				)
	return JsonResponse('On to Payment', safe=False)	
