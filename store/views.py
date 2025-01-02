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
        {"id": 1, "name": "Red Roses", "price": 25.99, "image_url": "static/assets/bouquet1.png"},
        {"id": 2, "name": "Sunflowers", "price": 18.99, "image_url": "static/assets/bouquet2.png"},
        {"id": 3, "name": "Pink Tulips", "price": 22.99, "image_url": "static/assets/bouquet3.png"},
        {"id": 4, "name": "Orchids", "price": 29.99, "image_url": "static/assets/bouquet4.png"},
        {"id": 5, "name": "Lavender Dreams", "price": 29.99, "image_url": "static/assets/bouquet5.png"},
        {"id": 6, "name": "Spring Bliss", "price": 21.99, "image_url": "static/assets/bouquet6.png"},
        {"id": 7, "name": "Floral Elegance", "price": 23.99, "image_url": "static/assets/bouquet7.png"},
        {"id": 8, "name": "Classic Red", "price": 20.99, "image_url": "static/assets/bouquet8.png"},
        {"id": 9, "name": "Ocean Blue", "price": 26.99, "image_url": "static/assets/bouquet9.png"},
        {"id": 10, "name": "Peach Paradise", "price": 28.99, "image_url": "static/assets/bouquet10.png"},
        {"id": 11, "name": "Pure White", "price": 24.99, "image_url": "static/assets/bouquet11.png"},
        {"id": 12, "name": "Blush Pink", "price": 22.99, "image_url": "static/assets/bouquet12.png"},
        {"id": 13, "name": "Romantic Charm", "price": 27.99, "image_url": "static/assets/bouquet13.png"},
        {"id": 14, "name": "Pastel Delight", "price": 21.99, "image_url": "static/assets/bouquet14.png"},
        {"id": 15, "name": "Springtime Bliss", "price": 29.99, "image_url": "static/assets/bouquet15.png"},
        {"id": 16, "name": "Vintage Elegance", "price": 30.99, "image_url": "static/assets/bouquet16.png"},
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