from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cart, CartItem
from products.models import Product

def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)
        size = request.POST.get('size', '')
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
            return JsonResponse({
                'success': True,
                'cart_total': str(cart.get_total_price()),
                'cart_empty': cart.items.count() == 0
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False})
    
    return JsonResponse({'success': False})

def update_cart(request, item_id):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            quantity = int(request.POST.get('quantity', 1))
            item.quantity = quantity
            item.save()
            
            return JsonResponse({
                'success': True,
                'item_total': str(item.get_total_price()),
                'cart_total': str(cart.get_total_price())
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False})
    
    return JsonResponse({'success': False})

def cart_count(request):
    cart = get_or_create_cart(request)
    count = sum(item.quantity for item in cart.items.all())
    return JsonResponse({'count': count})

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart