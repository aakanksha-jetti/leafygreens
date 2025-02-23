from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from home.models import veggies  # Import your Product model
from .models import CartItem
import stripe
# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST['username'] 
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')  
    else:
        return render(request,'login.html')
def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                messages.info(request,'User already exists')
                return redirect('login')
        else:
            messages.info(request,'password not matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request,'register.html')
def logout(request):
    auth.logout(request)
    return redirect('/')

def add_to_cart(request, product_id):
    product = get_object_or_404(veggies, pk=product_id)

    # Get the user's cart (using sessions or a database)
    # Example using sessions:
    if 'cart' not in request.session:
        request.session['cart'] = {}  # Initialize cart

    cart = request.session['cart']

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'quantity': 1}

    request.session.modified = True  # Important: Save the session

    return redirect('cart')  # Redirect to the cart page

# Example using CartItem model (more robust):
def add_to_cart_db(request, product_id):
    product = get_object_or_404(veggies, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product) # Gets or creates if doesn't exist.
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart') # Redirect to cart page
def cart(request):
    # Example using sessions:
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, data in cart.items():
        try:
            product = veggies.objects.get(pk=product_id)
            item_total = product.price * data['quantity']
            cart_items.append({'product': product, 'quantity': data['quantity'],'item_total': item_total})
            total+=item_total
        except veggies.DoesNotExist:
            # Handle the case where the product might have been deleted
            pass  # Or remove from cart: del cart[product_id]; request.session.modified = True
    if request.method == 'POST':  # Handle the Purchase button click
        # ***REPLACE THIS WITH REAL PAYMENT GATEWAY INTEGRATION***
        # This is a placeholder for a payment process.
        # In real code, you would:
        # 1. Create a payment intent or order with your payment gateway.
        # 2. Redirect the user to the gateway's checkout page (if needed).
        # 3. Handle the response from the gateway (success or failure).

        # Placeholder: Simulate a successful payment
        # You would get the payment intent from the payment gateway in real implementation.
        payment_intent = {'status': 'succeeded'} # Example: simulate payment intent

        if payment_intent['status'] == 'succeeded':
            # Clear the cart after successful purchase
            del request.session['cart']
            request.session.modified = True

            # Here you can save the order to your database
            # ... (your order creation logic)

            return render(request, 'order_confirmation.html')  # Redirect to confirmation page
        else:
            # Handle payment failure
            error_message = "Payment failed. Please try again."
            context = {'cart_items': cart_items, 'total': total, 'error_message': error_message}
            return render(request, 'cart.html', context)
    context = {'cart_items': cart_items, 'total': total}
    return render(request, 'cart.html', context)

# Example using CartItem model
def cart_db(request):
    cart_items = CartItem.objects.all() # Or filter by user if you have user-specific carts.
    total = sum(item.product.price * item.quantity for item in cart_items)
    context = {'cart_items': cart_items, 'total': total}
    return render(request, 'cart.html', context)
def remove_from_cart(request, product_id):
    # Example using sessions:
    if request.method == 'POST':  # Important: Only handle POST requests for removal
        cart = request.session.get('cart', {})

        if str(product_id) in cart: # convert product_id to string as session keys are strings
            del cart[str(product_id)]
            request.session.modified = True  # Crucial: Save the session changes

        return redirect('cart')  # Redirect back to the cart page

    return redirect('cart') 

# Example using CartItem model
def remove_from_cart_db(request, product_id):
    cart_item = CartItem.objects.get(product_id=product_id)
    cart_item.delete()
    return redirect('cart')
def checkout(request):
    return render(request, 'checkout.html')
