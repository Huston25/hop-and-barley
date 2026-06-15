from django.urls import path

from cart.views import CartAddView

app_name = 'orders'

urlpatterns = [
    path('cart/add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
]