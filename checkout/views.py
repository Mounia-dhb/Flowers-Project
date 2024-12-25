from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .checkout import Checkout
from cart.cart import Cart
from store.models import Order, Customer, CheckoutAddress, Profile
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from store.forms import UserInfoForm, UpdateUserForm, CheckoutForm
from django.views.generic import View
import paypalrestsdk

# PayPal Configuration
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "AcArGLlr2osY_RHsZzxiD5iyWRV-EppFCo21ErngvJk1770HDR1iph-88PXeZfEtaXHEhxrM5xI1bTgR",
    "client_secret": "EGT-bKpJVTRUXRwlelt9DliPepT_woefIlHS01J8RxI8JoU9rysd65A9AP1tVCWX4vggfQFHPACkLe48",
})

# Checkout Summary View
def checkout_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    # Handle unauthenticated users
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page

    try:
        current_user = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        current_user = None

    user_form = UpdateUserForm(request.POST or None, instance=current_user.user if current_user else None)
    form = UserInfoForm(request.POST or None, instance=request.user.profile if current_user else None)
    checkout_form = CheckoutForm(request.POST or None)

    context = {
        "form": form,
        "user_form": user_form,
        "checkout_form": checkout_form,
        "totals": totals,
        "quantities": quantities,
        "cart_products": cart_products,
    }
    return render(request, 'checkout.html', context)

# Create Payment View
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
        try:
            customer_firstname = request.POST.get('customer_firstname')
            customer_lastname = request.POST.get('customer_lastname')
            customer_phone = request.POST.get('customer_phone')
            customer_mail = request.POST.get('customer_email')

            checkout_customer = Customer(
                first_name=customer_firstname,
                last_name=customer_lastname,
                phone=customer_phone,
                email=customer_mail,
                password='',  # Add appropriate password logic if needed
            )
            checkout_customer.save()
        except Exception as e:
            messages.error(request, "An error occurred while creating the customer.")

        # Redirect to PayPal for payment
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        messages.error(request, "Payment creation failed. Please try again.")
        return render(request, 'payment_failed.html')

# Execute Payment View
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    try:
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            messages.success(request, "Payment executed successfully!")
            return render(request, 'payment_success.html')
        else:
            messages.error(request, "Payment execution failed.")
    except Exception as e:
        messages.error(request, "An error occurred while processing the payment.")
    return render(request, 'payment_failed.html')

# Payment Failed View
def payment_failed(request):
    return render(request, 'payment_failed.html')
