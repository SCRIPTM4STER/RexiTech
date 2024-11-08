from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models_product import Product, Category, Review
from .models_order import Cart, CartItem, Order
from .forms import ReviewForm, EditProfileForm, RegisterForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


# Display products and categories on the index page
def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'index.html', {'categories': categories, 'products': products})

# Add product to the cart view
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if enough stock is available before adding to the cart
    if product.stock < 1:
        return redirect('cart')  # Redirect back if no stock available
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # Set the initial quantity to 1 if the item is being added for the first time
    if created:
        cart_item.quantity = 1
    else:
        # If the item is already in the cart, just increment the quantity by 1
        cart_item.quantity += 1
    
    cart_item.save()

    # Decrease the product stock
    product.stock -= 1
    product.save()

    return redirect('cart')






# In the cart_view function
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.all() if cart else []
    total_price = sum([item.product.price * item.quantity for item in cart_items])  # Calculate the total price
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})


# Checkout and create an order
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return redirect('index')

    total_price = sum([item.product.price * item.quantity for item in cart.items.all()])
    order = Order.objects.create(
        user=request.user,
        email=request.user.email,
        total_price=total_price,
    )
    cart.delete()  # Clear the cart after the order is placed
    return render(request, 'store/checkout.html', {'order': order})


# Update cart item quantity
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product = cart_item.product

    # Get the new quantity from the POST request (ensure it's valid)
    new_quantity = int(request.POST.get('quantity', cart_item.quantity))
    
    # Check if the new quantity is valid (it shouldn't exceed available stock)
    if new_quantity > product.stock + cart_item.quantity:
        return redirect('cart')  # Redirect back if stock is insufficient
    
    # Update the cart item quantity and product stock accordingly
    product.stock += cart_item.quantity - new_quantity  # Adjust the stock based on the change
    product.save()

    cart_item.quantity = new_quantity
    cart_item.save()

    return redirect('cart')



# Remove product from the cart view
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product = cart_item.product
    
    # Increase the product stock by the quantity removed
    product.stock += cart_item.quantity
    product.save()
    
    # Remove the cart item
    cart_item.delete()

    return redirect('cart')



def product_detail(request, product_id):
    # Fetch the product based on the provided product_id
    product = get_object_or_404(Product, product_id=product_id)
    
    # Check if the product is out of stock
    is_out_of_stock = product.stock == 0
    
    # Handle the review form submission
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # Don't save to the database yet
            review.product = product  # Assign the current product to the review
            review.save()  # Save the review instance to the database
            return redirect('product_detail', product_id=product.product_id)  # Redirect using product_id
    else:
        form = ReviewForm()

    # Fetch all reviews related to this product
    reviews = Review.objects.filter(product=product)

    # Pass the product, review form, existing reviews, and out of stock status to the template
    context = {
        'product': product,
        'form': form,
        'reviews': reviews,
        'is_out_of_stock': is_out_of_stock,  # Pass the out of stock flag
    }
    return render(request, 'store/product_detail.html', context)




def category_detail(request, category_id):
    # Fetch the category based on the provided category_id
    category = get_object_or_404(Category, id=category_id)
    # Fetch all products belonging to this category
    products = Product.objects.filter(category=category)

    # Fetch all categories for the dropdown menu
    categories = Category.objects.all()

    context = {
        'category': category,
        'products': products,
        'categories': categories,  # Add categories to the context
    }
    return render(request, 'store/category.html', context)



def search(request):
    query = request.GET.get('query', '')  # Use .get() to avoid KeyError if 'query' is not in GET params

    if len(query) > 78:
        products = Product.objects.none()  # Return empty queryset if query is too long
    else:
        products = Product.objects.filter(name__icontains=query)  # Filter products by name (case-insensitive)

        # Update search history in session
        if query:
            search_history = request.session.get('search_history', [])
            if query not in search_history:
                search_history.insert(0, query)  # Add recent searches at the beginning
                search_history = search_history[:5]  # Limit history to the latest 5 searches
            request.session['search_history'] = search_history

    # Pass products, query, and search history to the template
    param = {
        'products': products,
        'query': query,
        'search_history': request.session.get('search_history', [])
    }
    return render(request, 'store/product_search.html', param)




def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /static/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")










# !auth views

def profile(request):
    return render(request, 'auth/profile.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
            else:
                user = form.save()
                messages.success(request, 'Registration successful.')
                # return redirect('index')
        else:
            messages.error(request, 'An error occurred during registration.')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render (request, 'index.html')




@login_required
def edit_profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user_profile, user=request.user)
    
    return render(request, 'auth/edit_profile.html', {'form': form})