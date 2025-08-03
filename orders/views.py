from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Order, OrderItem
from cart.models import Cart

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            address=request.POST['address'],
            city=request.POST['city'],
            postal_code=request.POST['postal_code'],
            phone=request.POST['phone'],
            total_amount=cart.get_total_price()
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                size=item.size
            )
        
        cart.items.all().delete()
        return redirect('orders:order_success', order_id=order.id)
    
    return render(request, 'orders/create_order.html', {'cart': cart})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})