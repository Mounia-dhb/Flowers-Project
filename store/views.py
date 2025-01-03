from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()

            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')
        return render(request, "update_info.html", {'form': form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()

            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')
        return render(request, "update_info.html", {'form': form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')

def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_user')
		else:
			form = ChangePasswordForm(current_user)
			# return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
def update_user(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user)
        user_form = UpdateUserForm(request.POST or None, instance=current_user.user)
        form = UserInfoForm(request.POST or None, instance=current_user)
        form_pass = ChangePasswordForm(current_user.user, request.POST)

        if user_form.is_valid():
            user_form.save()
			
            login(request, current_user.user)
            messages.success(request, "User Has Been Updated!!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form': user_form, 'form': form, 'form_pass': form_pass})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')


def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})	

def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')


def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})

from django.shortcuts import render

def home(request):
    context = {
        'bouquet_range': range(1, 17)
    }
    return render(request, 'home.html', context)

from django.shortcuts import render
def home(request):
    products = [
        {"id": 1, "name": "Elegant Blossoms", "price": "259.99 MAD", "image_url": "static/assets/bouquet1.png"},
        {"id": 2, "name": "Daisy Harmony", "price": "189.99 MAD", "image_url": "static/assets/bouquet2.png"},
        {"id": 3, "name": "Blush Bouquet", "price": "199.99 MAD", "image_url": "static/assets/bouquet3.png"},
        {"id": 4, "name": "Rose Garden", "price": "249.99 MAD", "image_url": "static/assets/bouquet4.png"},
        {"id": 5, "name": "Golden Glow", "price": "219.99 MAD", "image_url": "static/assets/bouquet5.png"},
        {"id": 6, "name": "Purple Radiance", "price": "289.99 MAD", "image_url": "static/assets/bouquet6.png"},
        {"id": 7, "name": "Ocean Whisper", "price": "209.99 MAD", "image_url": "static/assets/bouquet7.png"},
        {"id": 8, "name": "Cream Rose Charm", "price": "149.99 MAD", "image_url": "static/assets/bouquet8.png"},
        {"id": 9, "name": "Garnet Glow", "price": "199.99 MAD", "image_url": "static/assets/bouquet9.png"},
        {"id": 10, "name": "Berry Elegance", "price": "329.99 MAD", "image_url": "static/assets/bouquet10.png"},
        {"id": 11, "name": "Pure symphony", "price": "349.99 MAD", "image_url": "static/assets/bouquet11.png"},
        {"id": 12, "name": "Hydrangea Bloom", "price": "179.99 MAD", "image_url": "static/assets/bouquet12.png"},
        {"id": 13, "name": "Romantic Charm", "price": "309.99 MAD", "image_url": "static/assets/bouquet13.png"},
        {"id": 14, "name": "Gentle Bouquet", "price": "239.99 MAD", "image_url": "static/assets/bouquet14.png"},
        {"id": 15, "name": "Rose Harmony", "price": "199.99 MAD", "image_url": "static/assets/bouquet15.png"},
        {"id": 16, "name": "Vintage Elegance", "price": "259.99 MAD", "image_url": "static/assets/bouquet16.png"},
    ]
    return render(request, 'home.html', {'products': products})



def about(request):
	return render(request, 'about.html', {})	

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')



def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
			return redirect('update_info')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})