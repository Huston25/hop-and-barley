from django.urls import path

from .views import CartDetailView, CartItemDeleteView, CartItemQuantityUpdateView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('item/<int:item_id>/delete/', CartItemDeleteView.as_view(), name='cart_item_delete'),
    path('item/<int:item_id>/update/', CartItemQuantityUpdateView.as_view(), name='cart_item_update')
]