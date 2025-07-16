from urllib import request
from django.views import View
from . models import Product,Cart,Wishlist
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.

def login(request):
    return render(request, 'app/login.html')

def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')
  
def contact(request):
    return render(request, 'app/contact.html')

def login_view(request):
    return render(request, 'app/login.html')

class CategoryView(View):
  def get(self,reques,val):
    product = Product.objects.filter(category=val)
    title = Product.objects.filter(category=val).values('title')
    return render(request,"app/category.html",locals())
  
 

class ProductDetailView(View):  
    def get(self, request, pk,):
        product = get_object_or_404(Product, pk=pk)
        return render(request, "app/productdetail.html", {"product": product})

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  # Make sure you have this URL name
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomerRegistrationForm()
        return render(request, 'app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful! You are authenticated.")
            return redirect('home')  # Change 'home' to your actual URL name if needed
        else:
            messages.error(request, 'Invalid username or password.')
    
    # Render the login page in case of GET request or failed login
    return render(request, 'app/login.html')

@login_required
def profile(request):
    return render(request, 'app/profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('home')  # Replace with your login page URL name

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, "Added to cart!")
    return redirect('cart')

@login_required
def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, "Added to wishlist!")
    return redirect('wishlist')

@login_required
def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app/buy_now.html', {'product': product})

@login_required
def add_to_cart(request):
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    cart_item, created = Cart.objects.get_or_create(product=product, user=user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')  # or any other page you want to redirect to

def show_cart(request):
    return render(request, 'app/addtoCart.html', locals())