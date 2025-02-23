from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from .models import veggies
def home(request):
    items=veggies.objects.all()
    return render(request,'home.html',{'items':items})
def add_to_cart(request, veggie_id):
    if request.method == 'POST':
        veggie = get_object_or_404(veggies, pk=veggie_id)

        if 'cart' not in request.session:
            request.session['cart'] = {}
        cart = request.session['cart']

        if str(veggie_id) in cart:  # Convert veggie_id to string for session key
            cart[str(veggie_id)]['quantity'] = cart[str(veggie_id)].get('quantity', 1) + 1
        else:
            cart[str(veggie_id)] = {'quantity': 1}

        request.session.modified = True

        return JsonResponse({'message': f'{veggie.name} added to cart'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)