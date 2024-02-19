from django.urls import path
from . import views

urlpatterns = [
	path('', views.checkout_summary, name="checkout_summary"),
    path('save/', views.checkout_save, name="checkout_save"),
]
