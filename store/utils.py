import json
from . models import *

def cookieCart(request):
	try:

			cart = json.loads(request.COOKIES['cart'])
			print('Cart: ', cart)

	except:
			cart = {}
	items = []
	order = {'get_cart_total' :0.00, 'get_cart_items':0, 'shipping':False, 'get_cart_grand_total':0.00, 'needs_shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
			try:	
				cartItems += cart[i]["quantity"]
				product = Product.objects.get(id=i)
				total = (product.price * cart[i]["quantity"])

				order['get_cart_total'] +=  float ( total )
				order['get_cart_grand_total'] +=  float ( total )

				order['get_cart_items'] += cart[i]["quantity"]

				item = {
				'product':{
				'id':product.id,
				'name':product.name,
				'price':product.price,
				'image':product.image,
				'manufacturer':product.manufacturer,
				'digital':product.digital
				},
				'quantity':cart[i]["quantity"],
				'get_total':total
				}

				items.append(item)

				if product.digital == False:
					order['needs_shipping'] = True
			except:
				pass

			if order['needs_shipping'] == True:
				if order['get_cart_grand_total'] > 20:
					pass
				else: 
					order['get_cart_grand_total'] +=  float ( 5.99 )
						

	return { 'items' :items, 'order':order, 'cartItems':cartItems}

def cartData(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items

	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']
	return { 'items' :items, 'order':order, 'cartItems':cartItems}
	

def guestOrder(request, data):
		print('user not logged in')
		print('COOKIES', request.COOKIES)
		name = data['form']['name']
		lastname = data['form']['lastname']
		email = data['form']['email']
		
		cookieData = cookieCart(request)
		items = cookieData['items']

		customer, created = Customer.objects.get_or_create(
			email=email,

			)
		customer.name = name
		customer.lastname = lastname
		customer.save()

		order = Order.objects.create(
			customer=customer,
			complete=False,
			)
		for item in items:
			product = Product.objects.get(id=item['product']['id'])
			orderItem = OrderItem.objects.create(
				product=product,
				order=order,
				quantity=item['quantity']
				)
		return customer, order	