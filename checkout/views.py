from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .checkout import Checkout
from cart.cart import Cart
from store.models import Order, Customer, CheckoutAddress
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from store.forms import CheckoutForm
from django.views.generic import View
import paypalrestsdk



paypalrestsdk.configure({
    "mode": "sandbox", 
    "client_id": "AcArGLlr2osY_RHsZzxiD5iyWRV-EppFCo21ErngvJk1770HDR1iph-88PXeZfEtaXHEhxrM5xI1bTgR", # Updated
    "client_secret": "EGT-bKpJVTRUXRwlelt9DliPepT_woefIlHS01J8RxI8JoU9rysd65A9AP1tVCWX4vggfQFHPACkLe48", # Updated
})

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


def create_payment(request): 
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": request.POST.get('total_cmd'),  # Total amount in USD
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })
	
    if payment.create():   
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
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'payment_failed.html')
    
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')



def payment_failed(request):
    return render(request, 'payment_failed.html')