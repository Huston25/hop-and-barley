from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from cart.models import Cart, CartItem
from products.models import Product


# Create your views here.
class CartAddView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()
        return redirect('products:product_detail', slug=product.slug)


class CartDetailView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, 'cart.html', {'cart': cart, 'cart_items': cart.items.all()})


class CartItemDeleteView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def post(self, request, item_id):
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        cart_item.delete()
        return redirect('cart_detail')

class CartItemQuantityUpdateView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def post(self, request, item_id):
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )
        action = request.POST.get('action')

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
        cart_item.save()
        return redirect('cart_detail')