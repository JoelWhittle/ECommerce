from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
# Create your models here.


class Category(models.Model):		
	name = models.CharField(max_length=200, null=True)


	def __str__(self):
			return self.name

class Manufacturer(models.Model):
	name = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True)
	address_line_2 = models.CharField(max_length=200, null=True)

	city = models.CharField(max_length=200, null=True)
	county = models.CharField(max_length=200, null=True)
	country = models.CharField(max_length=200, null=True)

	postcode = models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(auto_now_add=True)
	telno = models.CharField(max_length=15, null=True)

	email = models.EmailField(max_length=200, null=True)


	def __str__(self):
			return self.name


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	lastname = models.CharField(max_length=200, null=True)
	telno = models.CharField(max_length=15, null=True)

	email = models.EmailField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200, null=True)
	manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, blank=True, null=True)

	price = models.DecimalField(max_digits=10, decimal_places=2)
	digital = models.BooleanField(default=False, null=True, blank=False)
	description = models.CharField(max_length=1000, null=True)
	image = models.ImageField(default='static/images/products/default.png', upload_to='static/images/products/')

	category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

	no_in_stock = models.IntegerField(default=0)

	def __str__(self):
		return self.name



class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False,null=True,blank=False)
	transaction_id = models.CharField(max_length=200, null=True)



	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()

		total = sum([item.get_total for item in orderitems])

		return total

	@property
	def get_cart_grand_total(self):
		orderitems = self.orderitem_set.all()
		if len(orderitems) == 0:
			return 0.00

		else:
			total = sum([item.get_total for item in orderitems])
			return total + Decimal(self.shipping_price)
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()

		total = sum([item.quantity for item in orderitems])
		return total
		


	@property
	def is_free_shipping(self):
		return self.get_cart_total > 20


	@property
	def shipping_price(self):

		if self.needs_shipping == False:
			return 0.00
		elif self.is_free_shipping:
			return 0.00
		else:
			return 5.99	
	@property
	def needs_shipping(self):
		shipping = False;
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping		

	def __str__(self):
		return str(self.id)


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	quantity = models.IntegerField(default=0, null=True,blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	
	def __str__(self):
		return str(self.id)

class ShippingAddress(models.Model):		
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	address = models.CharField(max_length=200, null=True)
	address_line_2 = models.CharField(max_length=200, null=True)

	city = models.CharField(max_length=200, null=True)
	county = models.CharField(max_length=200, null=True)
	country = models.CharField(max_length=200, null=True)

	postcode = models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
			return self.address

class ProductReview(models.Model):		
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
	rating = models.IntegerField(default=0)
	title = models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=1000, null=True)


	def __str__(self):
			return self.id



