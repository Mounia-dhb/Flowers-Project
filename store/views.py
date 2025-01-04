from django.shortcuts import render, redirect
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
        {"id": 1, "name": "Elegant Blossoms", "price": "259.99 MAD", "image_url": "assets/bouquet1.png", "description": (
            "Transform any occasion into a timeless celebration with Elegant Blossoms—a luxurious bouquet of pristine white roses, symbolizing purity and everlasting love. Handcrafted by expert florists, each bloom is carefully selected for its flawless beauty and complemented by lush, vibrant greenery."
            "\n\n"

            "Occasion Suggestion: Weddings, anniversaries, formal events, expressing sympathy, or as a gift to convey admiration and grace."
            "\n\n"

            "Order now to experience the epitome of floral artistry!"
            "\n\n"
            ),
        },
        
        {"id": 2, "name": "Daisy Harmony", "price": "189.99 MAD", "image_url": "assets/bouquet2.png", "description": (
            "Bring the sunshine indoors with Daisy Harmony, a cheerful arrangement of daisies that radiate happiness and charm. Each delicate white petal surrounds a golden center, evoking a sense of fresh beginnings and serenity. Tied with an elegant satin ribbon, this bouquet is perfect for celebrating small victories or simply bringing joy to a loved one."
            "\n\n"

            "Occasion Suggestion: Birthdays, congratulations, get-well-soon wishes, or as a bright “thinking of you” gesture."
            "\n\n"

            "Order today and spread the magic of daisies!"
            "\n\n"
            ),
        },
       
        {"id": 3, "name": "Blush Bouquet", "price": "199.99 MAD", "image_url": "assets/bouquet3.png", "description": (
            "Celebrate love and tenderness with the Blush Bouquet, a romantic mix of soft pink roses, vibrant red blooms, and pastel florals. Designed to exude charm and affection, this arrangement is perfect for occasions where words simply aren’t enough. Nestled in premium tissue paper, this bouquet is both luxurious and heartfelt."
            "\n\n"

            "Occasion Suggestion: Valentine’s Day, anniversaries, date nights, bridal showers, or any romantic gesture."
            "\n\n"

            "Make the moment unforgettable—order now!"
            "\n\n"
            ),
        },
        {"id": 4, "name": "Rose Garden", "price": "249.99 MAD", "image_url": "assets/bouquet4.png", "description": (
            "Indulge in the timeless beauty of Rose Garden, an exquisite bouquet of blush-pink roses set against a backdrop of eucalyptus leaves and elegant fillers. Evoking the serenity of a blooming garden, this arrangement is perfect for romantic occasions or as a thoughtful gesture of admiration."
            "\n\n"

            "Occasion Suggestion: Proposals, weddings, expressing gratitude, Mother’s Day, or as an elegant gift for someone special."
            "\n\n"

            "Order yours today and enchant your loved ones!"
            "\n\n"
            ),
        },
        {"id": 5, "name": "Golden Glow", "price": "219.99 MAD", "image_url": "assets/bouquet5.png", "description": (
            "Infuse your celebration with the vibrant warmth of Golden Glow, a radiant bouquet of yellow roses, daisies, and chrysanthemums. Designed to symbolize joy, friendship, and optimism, this arrangement is perfect for spreading cheer or celebrating meaningful milestones."
            "\n\n"

            "Occasion Suggestion: Birthdays, housewarmings, thank-you gifts, friendship day, or as a pick-me-up for a loved one."
            "\n\n"

            "Brighten someone’s day with this luminous creation—place your order now!"
            "\n\n"
            ),
        },
        {"id": 6, "name": "Purple Radiance", "price": "289.99 MAD", "image_url": "assets/bouquet6.png", "description": (
            "Step into a world of enchantment with Purple Radiance, a captivating bouquet of lavender roses, hydrangeas, and pastel accents. This arrangement is the epitome of sophistication, perfect for expressing admiration or creating a statement piece at upscale events."
            "\n\n"

            "Occasion Suggestion: Graduations, corporate gifts, formal celebrations, birthdays, or as a grand romantic gesture."
            "\n\n"

            "Experience the magic of Purple Radiance—order now!"
            "\n\n"
            ),
        },
        {"id": 7, "name": "Ocean Whisper", "price": "209.99 MAD", "image_url": "assets/bouquet7.png", "description": (
            "Embrace tranquility with Ocean Whisper, a serene bouquet inspired by the calming hues of the sea. Featuring soft blue hydrangeas and creamy white roses, this arrangement exudes elegance and peace."
            "\n\n"

            "Occasion Suggestion: Baby showers, housewarmings, sympathy gifts, or as a thoughtful gesture to celebrate new beginnings."
            "\n\n"

            "Order now to share the soothing charm of Ocean Whisper!"
            "\n\n"
            ),
        },
        {"id": 8, "name": "Cream Rose Charm", "price": "149.99 MAD", "image_url": "assets/bouquet8.png", "description": (
            "Delight in the understated elegance of Cream Rose Charm, a bouquet of creamy white roses that speak of sophistication and grace. Accented by subtle greenery and tied with a chic ribbon, this arrangement is perfect for any occasion."
            "\n\n"

            "Occasion Suggestion: Expressing sympathy, apologies, gratitude, or as a simple yet meaningful gift for any celebration."
            "\n\n"

            "Make someone feel special—order today!"
            "\n\n"
            ),
        },
        {"id": 9, "name": "Garnet Glow", "price": "199.99 MAD", "image_url": "assets/bouquet9.png", "description": (
            "A striking bouquet featuring deep red roses and delicate white lilies, adorned with soft green accents. Its bold and passionate tones create an unforgettable impression."
            "\n\n"

            "Occasion Suggestion: Perfect for romantic dates, festive occasions, or as a luxurious gift to express deep admiration."
            "\n\n"

            "Ignite passion and elegance—add this stunning bouquet to your cart today!"
            "\n\n"
            ),
        },
        {"id": 10, "name": "Berry Elegance", "price": "329.99 MAD", "image_url": "assets/bouquet10.png", "description": (
            "A sophisticated arrangement of rich burgundy and soft pink blooms, complemented by elegant foliage. This bouquet radiates charm and refined beauty."
            "\n\n"

            "Occasion Suggestion: Ideal for elegant dinners, corporate gifts, or as a thoughtful gesture to celebrate milestones."
            "\n\n"

            "Celebrate milestones with style—order this elegant bouquet now!"
            "\n\n"
            ),
        },
        {"id": 11, "name": "Pure Symphony", "price": "349.99 MAD", "image_url": "assets/bouquet11.png", "description": (
            "A graceful mix of white daisies and chrysanthemums, tied together with a modern wrapping for a clean and fresh look. This bouquet embodies simplicity and purity."
            "\n\n"

            "Occasion Suggestion: Best suited for weddings, congratulatory events, or as a symbol of new beginnings."
            "\n\n"

            "Embrace the beauty of simplicity—this bouquet is just a click away!"
            "\n\n"
            ),
        },
        {"id": 12, "name": "Hydrangea Bloom", "price": "179.99 MAD", "image_url": "assets/bouquet12.png", "description": (
            "A delicate arrangement of vibrant blue hydrangeas, wrapped in a soft pastel sheet to highlight its natural beauty. This bouquet offers a sense of tranquility and elegance."
            "\n\n"

            "Occasion Suggestion: Perfect for baby showers, housewarmings, or as a serene gift for someone special."
            "\n\n"
            
            "Bring calm and beauty into their life—order this serene bouquet today!"
            "\n\n"
            ),
        },
        {"id": 13, "name": "Romantic Charm", "price": "309.99 MAD", "image_url": "assets/bouquet13.png", "description": (
            "A breathtaking arrangement of soft pink and cream roses delicately intertwined with lush greenery. The bouquet exudes elegance and romantic allure, perfect for expressing heartfelt emotions."
            "\n\n"

            "Occasion Suggestion: Ideal for anniversaries, Valentine's Day, or as a romantic gesture to surprise your loved one."
            "\n\n"

            "Sweep them off their feet—order this timeless bouquet today!"
            "\n\n"
            ),
        },
        {"id": 14, "name": "Gentle Bouquet", "price": "239.99 MAD", "image_url": "assets/bouquet14.png", "description": (
            "An ethereal bouquet of pristine white flowers symbolizing purity and tranquility. This arrangement combines white roses, lilies, and eucalyptus for a fresh and timeless appeal."
            "\n\n"

            "Occasion Suggestion: Perfect for weddings, baby showers, or as a gift of peace and comfort in moments of reflection."
            "\n\n"

            "Embrace serenity—this bouquet is waiting for you!"
            "\n\n"
            ),
        },
        {"id": 15, "name": "Rose Harmony", "price": "199.99 MAD", "image_url": "assets/bouquet15.png", "description": (
            "A vibrant yet balanced arrangement of pink and white roses, harmoniously complemented by sprigs of greenery. This bouquet radiates joy and warmth."
            "\n\n"

            "Occasion Suggestion: A delightful choice for birthdays, graduations, or to simply brighten someone's day."
            "\n\n"

            "Share the joy—bring this cheerful bouquet home today!"
            "\n\n"
            ),
        },
        {"id": 16, "name": "Vintage Elegance", "price": "259.99 MAD", "image_url": "assets/bouquet16.png", "description": (
            "A charming bouquet of pastel-colored roses with subtle hints of peach and cream, creating a nostalgic yet sophisticated vibe. This arrangement is thoughtfully tied with a ribbon for a touch of vintage grace."
            "\n\n"

            "Occasion Suggestion: Perfect for Mother's Day, housewarming gifts, or as a centerpiece for elegant tea parties."
            "\n\n"

            "Add a touch of nostalgia to your moments—order now!"
            "\n\n"
            ),
        },
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
    

from django.http import JsonResponse

def cart_add(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('product_qty')

        # Simulate adding to cart (or implement your logic)
        cart = request.session.get('cart', {})
        cart[product_id] = quantity
        request.session['cart'] = cart

        # Respond with success and updated cart quantity
        return JsonResponse({'success': True, 'qty': sum(map(int, cart.values()))})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


from django.shortcuts import render

def cart_summary(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    # Assume `Product` is your model for products
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        total += product.price * int(qty)
        products.append({'product': product, 'quantity': qty})

    return render(request, 'cart_summary.html', {'products': products, 'total': total})

