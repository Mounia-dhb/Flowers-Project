from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .checkout import Checkout
from cart.cart import Cart
from store.models import Order, Customer, CheckoutAddress
from django.http import JsonResponse
from django.contrib import messages
from store.forms import CheckoutForm
from django.views.generic import View

def checkout_summary(request):
    # Get checkout form
    form = CheckoutForm()
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    context = {
        "form": form,
        "totals":totals,
		"quantities":quantities, 
        "cart_products":cart_products
    }
    return render(request, 'checkout.html', context)   

def checkout_save(request):
	form = CheckoutForm()
	if request.method == "POST":
		form = CheckoutForm(request.POST)
		if form.is_valid():
			# Get stuff
			customer_firstname = request.POST.get('customer_firstname')
			customer_lastname = request.POST.get('customer_lastname')
			customer_phone = request.POST.get('customer_phone')
			customer_mail = request.POST.get('customer_email')

			checkout_customer = Customer(
				first_name=customer_firstname,
				last_name=customer_lastname,
				phone=customer_phone,
				email=customer_mail,
				password=''
			)
			checkout_customer.save()
			messages.success(request, ("Customer  created ..."))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem creating, please try again..."))
			return redirect('checkout')
	else:
		return render(request, 'checkout.html', {'form':form})