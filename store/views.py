from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm


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
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
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
    return render(request, 'category_summary.html', {"categories": categories})


def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.success(request, "That Category Doesn't Exist...")
        return redirect('home')


def product(request, pk):
    products = [
        {"id": 1, "name": "Elegant Blossoms", "price": "259.99 MAD", "image_url": "static/assets/bouquet1.png", "description": "A classic arrangement of delicate flowers."},
        {"id": 2, "name": "Daisy Harmony", "price": "189.99 MAD", "image_url": "static/assets/bouquet2.png", "description": "Bright daisies to bring joy to your day."},
        {"id": 3, "name": "Blush Bouquet", "price": "199.99 MAD", "image_url": "static/assets/bouquet3.png", "description": "Blush pink flowers for a romantic touch."},
        {"id": 4, "name": "Rose Garden", "price": "249.99 MAD", "image_url": "static/assets/bouquet4.png", "description": "An elegant collection of the finest roses."},
        {"id": 5, "name": "Golden Glow", "price": "219.99 MAD", "image_url": "static/assets/bouquet5.png", "description": "Golden blooms to brighten any room."},
        {"id": 6, "name": "Purple Radiance", "price": "289.99 MAD", "image_url": "static/assets/bouquet6.png", "description": "Sophisticated purple flowers for any occasion."},
        {"id": 7, "name": "Ocean Whisper", "price": "209.99 MAD", "image_url": "static/assets/bouquet7.png", "description": "A serene mix of blue and white blooms."},
        {"id": 8, "name": "Cream Rose Charm", "price": "149.99 MAD", "image_url": "static/assets/bouquet8.png", "description": "Soft cream roses arranged with elegance."},
        {"id": 9, "name": "Garnet Glow", "price": "199.99 MAD", "image_url": "static/assets/bouquet9.png", "description": "Rich red flowers to make a bold statement."},
        {"id": 10, "name": "Berry Elegance", "price": "329.99 MAD", "image_url": "static/assets/bouquet10.png", "description": "Deep red and berry tones for a luxurious look."},
        {"id": 11, "name": "Pure Symphony", "price": "349.99 MAD", "image_url": "static/assets/bouquet11.png", "description": "A symphony of white and cream flowers."},
        {"id": 12, "name": "Hydrangea Bloom", "price": "179.99 MAD", "image_url": "static/assets/bouquet12.png", "description": "Hydrangeas in full bloom to captivate."},
        {"id": 13, "name": "Romantic Charm", "price": "309.99 MAD", "image_url": "static/assets/bouquet13.png", "description": "Roses and lilies for a romantic gesture."},
        {"id": 14, "name": "Gentle Bouquet", "price": "239.99 MAD", "image_url": "static/assets/bouquet14.png", "description": "Soft pastel flowers arranged delicately."},
        {"id": 15, "name": "Rose Harmony", "price": "199.99 MAD", "image_url": "static/assets/bouquet15.png", "description": "A harmonious blend of roses in various shades."},
        {"id": 16, "name": "Vintage Elegance", "price": "259.99 MAD", "image_url": "static/assets/bouquet16.png", "description": "Timeless flowers with a vintage appeal."},
    ]

    product = next((item for item in products if item["id"] == pk), None)
    if not product:
        return render(request, "404.html", {"error": "Product not found."})

    return render(request, 'product.html', {'product': product})


def home(request):
    products = [
        {"id": 1, "name": "Elegant Blossoms", "price": "259.99 MAD", "image_url": "static/assets/bouquet1.png", "description": "A classic arrangement of delicate flowers."},
        {"id": 2, "name": "Daisy Harmony", "price": "189.99 MAD", "image_url": "static/assets/bouquet2.png", "description": "Bright daisies to bring joy to your day."},
        {"id": 3, "name": "Blush Bouquet", "price": "199.99 MAD", "image_url": "static/assets/bouquet3.png", "description": "Blush pink flowers for a romantic touch."},
        {"id": 4, "name": "Rose Garden", "price": "249.99 MAD", "image_url": "static/assets/bouquet4.png", "description": "An elegant collection of the finest roses."},
        {"id": 5, "name": "Golden Glow", "price": "219.99 MAD", "image_url": "static/assets/bouquet5.png", "description": "Golden blooms to brighten any room."},
        {"id": 6, "name": "Purple Radiance", "price": "289.99 MAD", "image_url": "static/assets/bouquet6.png", "description": "Sophisticated purple flowers for any occasion."},
        {"id": 7, "name": "Ocean Whisper", "price": "209.99 MAD", "image_url": "static/assets/bouquet7.png", "description": "A serene mix of blue and white blooms."},
        {"id": 8, "name": "Cream Rose Charm", "price": "149.99 MAD", "image_url": "static/assets/bouquet8.png", "description": "Soft cream roses arranged with elegance."},
        {"id": 9, "name": "Garnet Glow", "price": "199.99 MAD", "image_url": "static/assets/bouquet9.png", "description": "Rich red flowers to make a bold statement."},
        {"id": 10, "name": "Berry Elegance", "price": "329.99 MAD", "image_url": "static/assets/bouquet10.png", "description": "Deep red and berry tones for a luxurious look."},
        {"id": 11, "name": "Pure Symphony", "price": "349.99 MAD", "image_url": "static/assets/bouquet11.png", "description": "A symphony of white and cream flowers."},
        {"id": 12, "name": "Hydrangea Bloom", "price": "179.99 MAD", "image_url": "static/assets/bouquet12.png", "description": "Hydrangeas in full bloom to captivate."},
        {"id": 13, "name": "Romantic Charm", "price": "309.99 MAD", "image_url": "static/assets/bouquet13.png", "description": "Roses and lilies for a romantic gesture."},
        {"id": 14, "name": "Gentle Bouquet", "price": "239.99 MAD", "image_url": "static/assets/bouquet14.png", "description": "Soft pastel flowers arranged delicately."},
        {"id": 15, "name": "Rose Harmony", "price": "199.99 MAD", "image_url": "static/assets/bouquet15.png", "description": "A harmonious blend of roses in various shades."},
        {"id": 16, "name": "Vintage Elegance", "price": "259.99 MAD", "image_url": "static/assets/bouquet16.png", "description": "Timeless flowers with a vintage appeal."},
    ]
    return render(request, 'home.html', {'products': products})


def product_detail(request, pk):
    products = [
        {"id": 1, "name": "Elegant Blossoms", "price": "259.99 MAD", "image_url": "static/assets/bouquet1.png", "description": "A classic arrangement of delicate flowers."},
        {"id": 2, "name": "Daisy Harmony", "price": "189.99 MAD", "image_url": "static/assets/bouquet2.png", "description": "Bright daisies to bring joy to your day."},
        {"id": 3, "name": "Blush Bouquet", "price": "199.99 MAD", "image_url": "static/assets/bouquet3.png", "description": "Blush pink flowers for a romantic touch."},
        {"id": 4, "name": "Rose Garden", "price": "249.99 MAD", "image_url": "static/assets/bouquet4.png", "description": "An elegant collection of the finest roses."},
        {"id": 5, "name": "Golden Glow", "price": "219.99 MAD", "image_url": "static/assets/bouquet5.png", "description": "Golden blooms to brighten any room."},
        {"id": 6, "name": "Purple Radiance", "price": "289.99 MAD", "image_url": "static/assets/bouquet6.png", "description": "Sophisticated purple flowers for any occasion."},
        {"id": 7, "name": "Ocean Whisper", "price": "209.99 MAD", "image_url": "static/assets/bouquet7.png", "description": "A serene mix of blue and white blooms."},
        {"id": 8, "name": "Cream Rose Charm", "price": "149.99 MAD", "image_url": "static/assets/bouquet8.png", "description": "Soft cream roses arranged with elegance."},
        {"id": 9, "name": "Garnet Glow", "price": "199.99 MAD", "image_url": "static/assets/bouquet9.png", "description": "Rich red flowers to make a bold statement."},
        {"id": 10, "name": "Berry Elegance", "price": "329.99 MAD", "image_url": "static/assets/bouquet10.png", "description": "Deep red and berry tones for a luxurious look."},
        {"id": 11, "name": "Pure Symphony", "price": "349.99 MAD", "image_url": "static/assets/bouquet11.png", "description": "A symphony of white and cream flowers."},
        {"id": 12, "name": "Hydrangea Bloom", "price": "179.99 MAD", "image_url": "static/assets/bouquet12.png", "description": "Hydrangeas in full bloom to captivate."},
        {"id": 13, "name": "Romantic Charm", "price": "309.99 MAD", "image_url": "static/assets/bouquet13.png", "description": "Roses and lilies for a romantic gesture."},
        {"id": 14, "name": "Gentle Bouquet", "price": "239.99 MAD", "image_url": "static/assets/bouquet14.png", "description": "Soft pastel flowers arranged delicately."},
        {"id": 15, "name": "Rose Harmony", "price": "199.99 MAD", "image_url": "static/assets/bouquet15.png", "description": "A harmonious blend of roses in various shades."},
        {"id": 16, "name": "Vintage Elegance", "price": "259.99 MAD", "image_url": "static/assets/bouquet16.png", "description": "Timeless flowers with a vintage appeal."},
    ]

    product = next((item for item in products if item["id"] == pk), None)
    if not product:
        return render(request, "404.html", {"error": "Product not found."})

    return render(request, 'product.html', {'product': product})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There was an error, please try again...")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...Thanks for stopping by...")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Username Created - Please Fill Out Your User Info Below...")
            return redirect('update_info')
        else:
            messages.success(request, "Whoops! There was a problem Registering, please try again...")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
