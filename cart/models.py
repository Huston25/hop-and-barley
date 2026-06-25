from django.contrib.auth.models import User
from django.db import models

from config import settings
from products.models import Product


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)


    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'


# from decimal import Decimal
# from django.shortcuts import get_object_or_404
# from products.models import Product
#
# class Cart:
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get('cart', {})
#         if not cart:
#             cart = self.session['cart'] = {}
#         self.cart = cart
#     def add(self, product, quantity=1, override_quantity=False):
#         product_id = str(product.id)
#         cart_key = product_id
#
#         if cart_key not in self.cart:
#             self.cart[cart_key] = {'quantity': 0, 'price': str(product.price), 'product_id': product_id}
#         if override_quantity:
#             self.cart[cart_key]['quantity'] = override_quantity
#         else:
#             self.cart[cart_key]['quantity'] += quantity
#         self.save()
#
#     def save(self):
#         self.session.modified = True
#
#     def remove(self, product):
#         product_id = str(product.id)
#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()
#
#     def update_quantity(self, product, quantity):
#         if quantity <= 0:
#             self.remove(product)
#         else:
#             self.add(product, override_quantity=quantity)
#
#     def __iter__(self):
#         product_ids = [item['product_id'] for item in self.cart.values()]
#         products = Product.objects.filter(id__in=product_ids)
#         cart = self.cart.copy()
#
#         for product in products:
#             for cart_key, cart_item in cart.items():
#                 if cart_item['product_id'] == str(product.id):
#                     cart_item['product'] = product
#                     cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
#                     yield cart_item
#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def get_total_price(self):
#         return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
#
#     def clear(self):
#         self.session.pop('cart', None)
#         self.save()
#
#     def get_cart(self):
#         items = []
#         for item in self:
#             items.append({
#                 'product': item['product'],
#                 'quantity': items['quantity'],
#                 'price': Decimal(item['price']),
#                 'total_price': item['total_price'],
#                 'cart_key': f'{item["product_id"]}'
#             })
#         return items
#
#     def __str__(self):
#         return f"Cart for {self.user}"